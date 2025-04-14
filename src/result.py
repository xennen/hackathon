import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from ChannelAttribution import markov_model, heuristic_models


def attribution(dir):
    # считываем таблички в датафреймы
    costs = pd.read_csv(f'{dir}/costs.csv')
    visits = pd.read_csv(f'{dir}/visits.csv')
    orders = pd.read_csv(f'{dir}/orders.csv')

    # работаем с формата дат
    costs['dt'] = pd.to_datetime(costs['dt']).dt.normalize()
    visits['date'] =  pd.to_datetime(visits['Session Start']).dt.normalize()

    # работаем с формата дат и времени
    visits['Session Start'] = pd.to_datetime(visits['Session Start'])
    visits['Session End'] = pd.to_datetime(visits['Session End'])
    orders['Event Dt'] = pd.to_datetime(orders['Event Dt'])

    # создаем вспомогательную таблицу с датой старта когорты для расчета объема трафика
    first_df = visits.loc[visits['date'] <= costs['dt'].max()]\
    .sort_values(by='Session Start', ascending=True)\
    .groupby(['User Id'])\
    .agg(first_date = ('Session Start', 'min'), Channel = ('Channel', 'first'))\
    .reset_index()
    first_df['first_date'] = first_df['first_date'].dt.normalize()

    # добавляем в табличку costs объем трафика
    new_data = first_df.groupby(['first_date', 'Channel']).agg(traffic = ('User Id', 'nunique')).reset_index().rename(columns = {'first_date': 'dt'})
    costs = costs.merge(new_data, on = ['dt', 'Channel'], how = 'left')
    costs['cpu'] = costs['costs'] / costs['traffic']

    # вывод метрик для расчетов в гугл-шитах
    costs.groupby('Channel')[['costs', 'traffic']].sum()

    # добавляем дату старта когорты в orders, работаем с форматами дат
    orders = orders.merge(first_df[['User Id', 'first_date']], on = 'User Id', how = 'left')
    orders['date'] = pd.to_datetime(orders['Event Dt']).dt.normalize()
    orders['days'] = (orders['date'] - orders['first_date']).dt.days

    # определяем крайнюю дату с учетом расчетного периода для LTV 60 дней
    max_first_date = orders['first_date'].max() - timedelta(days=60)

    # оцениваем за LTV 60 дней
    ltv = orders.groupby('User Id').agg(Revenue2M = ('Revenue', 'sum'), first_pay_tm = ('Event Dt', 'min')).reset_index()

    # отсекаем сессии перед первой оплатой и привязывааем к первой оплате весь LTV за 60 дней
    data_pre = visits.loc[visits['date'] <= costs['dt'].max()].merge(ltv, on = 'User Id', how = 'inner')

    data_pre = data_pre.loc[
        (data_pre['first_pay_tm'] >= data_pre['Session Start']) &
        (data_pre['first_pay_tm'] <= data_pre['Session End'])
    ]

    data = visits.loc[(visits['date'] <= costs['dt'].max()) & (visits['date'] <= max_first_date)]\
    .merge(data_pre, on=['User Id', 'Region', 'Device', 'Channel', 'Session Start', 'Session End', 'date'], how='left')

    # добавляем нужные поля для дальнейшей фильтрации
    data['Revenue2M'] = data['Revenue2M'].fillna(0)
    data['Revenue2M_cum'] = data.groupby('User Id')['Revenue2M'].transform('sum')
    data['first_pay_tm_all'] = data.groupby('User Id')['first_pay_tm'].transform('min')
    data['is_converted'] = np.where(data['Revenue2M_cum'] > 0, 1, 0)

    # собираем финальный датасет по вышеописанной логике отдельно для платников, отдельно для бесплатников и склеиваем вместе
    data_payers = data.loc[data['is_converted'] == 1]
    data_payers = data_payers.loc[data_payers['Session Start'] <= data_payers['first_pay_tm_all']]
    data_nonpayers = data.loc[data['is_converted'] == 0]
    new_data = pd.concat([data_payers, data_nonpayers], axis = 0)

    # приводим датасет к формату цепочек
    df = new_data.sort_values(by = ['User Id', 'Session Start'])\
    .groupby('User Id')\
    .agg({'Channel': 'unique','first_pay_tm': 'count', 'Revenue2M': 'sum'})\
    .reset_index()

    df = df.rename(columns = {'first_pay_tm': 'conversion',
                            'Revenue2M': 'value'})

    # фильтруем датасет только по пользователям с цепочками (опционально, для других целей можно исключить)
    df['Channel2'] = df['Channel'].apply(lambda x: len(x))
    df = df.loc[df['Channel2'] > 1]

    # пишем функцию для преобразования цепочек
    def listToString(df):
        str1 = ""
        for i in df['Channel']:
            str1 += i + ' > '
        return str1[:-3]

    # применяем функцию для преобразования цепочек
    df['Channel'] = df.apply(listToString, axis=1)


    # готовим датасет для передачи в библиотека для моделирования атрибуции оплат
    df['null'] = np.where(df['conversion'] == 0,1,0)
    ndf = df.groupby('Channel').agg({'User Id': 'nunique', 'conversion': 'sum', 'null': 'sum', 'value': 'sum'}).reset_index()
    ndf = ndf.rename(columns={"User Id":"unique_users", "conversion":"total_conversions", "null": "total_null", "value": "total_value"})

    # моделиуем атрибуцию оплат по цепям Маркова
    M = markov_model(ndf, "Channel", "total_conversions", var_value="total_value", flg_adv=False)

    # моделиуем атрибуцию оплат по классическим моделям (первое / последнее касание / линейная)
    H = heuristic_models(ndf,"Channel","total_conversions",var_value="total_value", flg_adv=False)

    # объединяем результаты и выводим график / отчет
    R = pd.merge(H, M, on="channel_name", how="inner")
    R1 = R[["channel_name","first_touch_conversions","last_touch_conversions", "linear_touch_conversions","total_conversions"]]
    R1.columns=["channel_name","first_touch","last_touch","linear_touch","markov_model"]
    R1 = pd.melt(R1, id_vars="channel_name")
    
    return R1