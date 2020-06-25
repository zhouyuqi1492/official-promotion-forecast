# 官员升职时间预测

本项目是北京大学软件与微电子学院数据挖掘课程的期末大作业，项目的主要内容是根据官员的基本信息，来预测其下次升职所需要的时间。基于sklearn实现了十种常见的机器学习算法关于该项目回归问题的运用，并尝试使用多模型集成的方法获得结果进一步的提升。本项目的详细报告在word文件“官员晋升时间预测项目报告”中。

## 项目报告目录

1. 数据获取
2. 数据预处理
3. 模型训练
4. 模型集成
5. 项目总结

## 文件说明

1. 'dfzlk_spider.py' 文件从人民网爬取中国地方官员的基本信息，获取后以json格式存入data文件夹。
2. 'official.py'为官员类，存储官员的基本信息与经历信息。
3. 'expMap.py'文件用于官员职位映射功能。
4. '官员晋升时间预测-最终版.ipynb'包含了特征分析，模型训练，项目总结等，为总文件。
5. '数据挖掘期末作业：官员晋升时间预测项目报告.docx'文件为项目综述，用于上交作业的报告。


# Official promotion time forecast

This project is the final assignment of the data mining course of the School of Software and Microelectronics at Peking University. The main content of the project is to predict the time required for the next promotion based on the basic information of the officials. Based on sklearn, ten common machine learning algorithms are used to implement the regression problem of the project, and the method of multi-model integration is used to obtain further improvement of the results. The detailed report of this project is in the word file "Report of the Official Promotion Time Prediction Project".

## Project Report Directory

1. Data Acquisition
2. Data preprocessing
3. Model training
4. Model integration
5. Project summary

## File description

1. The'dfzlk_spider.py' file crawls the basic information of Chinese local officials from People's Net, and saves it in the data folder in json format.
2.'official.py' is an official category, storing basic information and experience information of officials.
3. The'expMap.py' file is used for the official position mapping function.
4.'Official promotion time prediction-final version. ipynb' contains feature analysis, model training, project summary, etc., as a total file.
5.'Data mining final operation: official promotion time prediction project report.docx' file is a summary of the project, which is used for the report of the operation.
