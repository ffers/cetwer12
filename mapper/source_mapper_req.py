


class SourceMap:
    @staticmethod
    def map(req):
        data = (
            req.form['article'],
            req.form['name'],
            req.form['price'],
            0,
            0
        )
        return data