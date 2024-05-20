from datetime import datetime
import motor.motor_asyncio


async def get_salaries_by_group(dt_from, dt_upto, group_type):
    group_type_format = {
        'hour': '%Y-%m-%dT%H',
        'day': '%Y-%m-%d',
        'month': '%Y-%m'
    }

    dt_from = datetime.strptime(dt_from, '%Y-%m-%dT%H:%M:%S')
    dt_upto = datetime.strptime(dt_upto, '%Y-%m-%dT%H:%M:%S')

    uri = 'mongodb://localhost:27017/'
    client = motor.motor_asyncio.AsyncIOMotorClient(uri)
    db = client['data']
    data = db['data']

    query = [
        {
            '$match': {
                'dt': {
                    '$gte': dt_from,
                    '$lte': dt_upto,
                }
            }
        },
        {
            '$group': {
                '_id': {
                    '$dateToString': {
                        'date': '$dt',
                        'format': group_type_format[group_type]
                    }
                },
                'total_value': {
                    '$sum': '$value'
                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'date': '$_id',
                'total_value': 1
            }
        },
        {
            '$sort':
                {
                    'date': 1
                }
        }
    ]

    res = data.aggregate(query)
    res = await res.to_list(length=None)

    salaries = {'dataset': [], 'labels': []}

    for i in res:
        salaries['dataset'].append(i['total_value'])
        formatted_date = datetime.strptime(i['date'], group_type_format[group_type])
        salaries['labels'].append(formatted_date)

    return salaries
