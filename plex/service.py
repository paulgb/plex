from .sequential_runner import SequentialRunner


class Service:
    def __init__(self):
        self.runner = SequentialRunner()

    def send_message(self, message):
        if message['message'] == 'update_cell':
            result = self.runner.set_cell(message['index'], message['value'])
            for index, status in result:
                yield {
                    'message': 'cell_status',
                    'index': index,
                    'status': status.to_dict(),
                }
        else:
            raise ValueError(f'Unknown message type `{message["message"]}`')
