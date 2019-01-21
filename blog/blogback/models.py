from django.db import models


class User(models.Model):
    username = models.CharField(max_length=10, unique=True)
    # 设置150是为了加密
    password = models.CharField(max_length=150, null=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'


class ArticleType(models.Model):
    t_name = models.CharField(max_length=10, unique=True)
    # t_id = models.ForeignKey('self', on_delete=models.CASCADE)
    #
    class Meta:
        db_table = 'article_type'
    #
    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'types': self.t_name,
    #         'article_count': self.article_set.count(),
    #         't_id': self.t_id,
    #     }


class Article(models.Model):
    title = models.CharField(max_length=30, null=False)
    t_name = models.ForeignKey(ArticleType, null=False, on_delete=models.CASCADE)
    is_show = models.BooleanField(default=False)
    # 描述
    desc = models.CharField(max_length=100, null=True)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'article'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            't_name': self.t_name,
            'desc': self.desc,
            'is_show': self.is_show,
            'content': self.content,
            'create_time': self.create_time.strftime('%Y-%m-%d')
        }
