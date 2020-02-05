import xlsxwriter

class Writer():
    @staticmethod
    def csv_writer(out_file, df):
        df.toPandas().to_csv(out_file, index=False)

    @staticmethod
    def excel_writer(out_file, df):
        df.to_excel(out_file, engine='xlsxwriter')

    @staticmethod
    def write_list(out_file, out_list, mode='w+'):
        with open(out_file, mode) as file:
            for item in out_list:
                file.write('%s\n' % item)

