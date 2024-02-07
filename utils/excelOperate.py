import xlrd

def get_params(filename,sheet_name):
    file = xlrd.open_workbook(filename)
    sheet = file.sheet_by_name(sheet_name)
    rows = sheet.nrows
    ncols = sheet.ncols
    # 初始化变量列表
    dic_params = []

    # 遍历每行
    for row in range(1,rows):
        dic = {}
        for ncol in range(1,ncols):
            key = sheet.row(0)[ncol].value
            value = sheet.row(row)[ncol].value
            if type(value) == float:
                dic[key] = str(int(value)).strip("\t")
            else:
                dic[key] = str(value).strip("\t")
        if 'call_id' in dic.keys() :
            if dic['call_id'] != 'no' :
                dic_params.append(dic)
    return dic_params



