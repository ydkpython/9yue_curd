from yingun.service import v1
from app02 import models


v1.site.register(models.Myclass)
v1.site.register(models.Youclass)