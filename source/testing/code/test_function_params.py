import inspect


def stupid_function_name(a=2, b=4, c=None):
    print(locals())  # gives the parameters and their values
    print(inspect.stack()[0][3])  # gives the function name
    print(inspect.stack()[1][3])  # gives the function name that called this function


def der():
    stupid_function_name()


der()

'''
await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                 message_text={
                                                                     'function': inspect.stack()[0][3],
                                                                     'locals': locals(),
                                                                     'caller': inspect.stack()[1][3]})
'''
