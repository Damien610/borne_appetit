# Handler Lambda Python
def health(event, context):
    return {
        'statusCode': 200,
        'body': '{"status": "healthy"}'
    }
