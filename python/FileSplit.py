# coding=gbk
import os

# Ҫ�ָ���ļ�
source_file = 'C:\\Users\\ChuangLan\\Desktop\\202_201910101720166.txt'

# ����ÿ�����ļ�������
file_count = 1000000  # ������Ҫ�Զ���


def mk_SubFile(lines, srcName, sub):
    [des_filename, extname] = os.path.splitext(srcName)
    filename = des_filename + '_' + str(sub) + extname
    print('�����������ļ�: %s' % filename)
    with open(filename, 'w' , encoding='UTF-8') as fout:
        fout.writelines(lines)
        return sub + 1


def split_By_LineCount(filename, count):
    with open(filename, 'r' , encoding='gbk') as fin:
        buf = []
        sub = 1
        for line in fin:
            if len(line.strip()) > 0:  # ��������
                buf.append(line)
                # �����������ָ��������������Ϊһ�������ļ�¼����bufд�뵽һ�����ļ��У�����ʼ��buf
                line_tag = line.strip()[0]  # ȡÿһ�е�һ���ַ����������Ϊ�գ��ᱨ��,�ʼ���ǰ���ж�
                if len(buf) >= count :  # ÿһ���µļ�¼�����Ǵ�*��ʶ��ʼ
                    buf = buf[:-1]
                    sub = mk_SubFile(buf, filename, sub)  # ��bufд�����ļ���
                    buf = [line]  # ��ʼ����һ�����ļ���buf����һ��Ϊ*��ͷ��

        # ���һ���ļ����ļ��������ܲ���ָ������
        if len(buf) != 0:
            sub = mk_SubFile(buf, filename, sub)
    print("ok")


if __name__ == '__main__':
    split_By_LineCount(source_file, file_count)  # Ҫ�ָ���ļ�����ÿ�����ļ�������
