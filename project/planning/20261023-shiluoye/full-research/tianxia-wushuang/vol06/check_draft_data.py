"""研究草稿编排数据的轻量结构诊断。"""
from scene_data import SCENES_DATA
for x in SCENES_DATA:
    if len(x)!=13:print(x[0],len(x),x)
