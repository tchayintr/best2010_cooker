'''
    Rule-based for denoising BEST2010 corpus
    See README.md for more details
'''

CASES = [('<NE>กรุงเทพ</NE', '<NE>กรุงเทพ</NE>'),
         ('<NE>Surin>Pitsuwan</NE>', '<NE>Surin Pitsuwan</NE>'),
         ('<NE>NE>Hill, Michael</NE>', '<NE>Hill, Michael</NE>'),
         ('<NE>NE>วลาดิเมียร์ กาบูลอฟ</NE>', '<NE>วลาดิเมียร์ กาบูลอฟ</NE>'),
         ('<NE>NE>แกเร็ธ แบร์รี่</NE>', '<NE>แกเร็ธ แบร์รี่</NE>'),
         ('<NE>NE>บราซิล</NE>', '<NE>บราซิล</NE>'),
         ('<NE>NE>จ.ร้อยเอ็ด</NE>', '<NE>จ.ร้อยเอ็ด</NE>'),
         ('<NE>โรงพยาบาลนราธิวาส</NE</NE>', '<NE>โรงพยาบาลนราธิวาส</NE>'),
         ('<NE>เช็ก</NE</NE>', '<NE>เช็ก</NE>'),
         ('<NE>ไอ้ธาร</NE</NE>', '<NE>ไอ้ธาร</NE>'),
         ('<NE>ยุโรป/NE></NE>', '<NE>ยุโรป</NE>'),
         ('<NE>ป.ป.ช./NE></NE>', '<NE>ป.ป.ช.</NE>'),
         ('<NE>วธ./NE></NE>', '<NE>วธ.</NE>'),
         ('<NE>พม./NE></NE>', '<NE>พม.</NE>'),
         ('<NE>นักโทษเด็ดขาดชาย<ชด พุ่มไหว</NE>',
          '<NE>นักโทษเด็ดขาดชายชด พุ่มไหว</NE>'),
         ('<NE>Brandes,E.<W.</NE>', '<NE>Brandes,E.W.</NE>'),
         ('AB>พ.ศ.</AB>', '<AB>พ.ศ.</AB>'),
         ('<NE>จังหวัดอุบลราชธานี></NE>', '<NE>จังหวัดอุบลราชธานี</NE>'),
         ('<NE>สปส.></NE>', '<NE>สปส.</NE>'),
         ('<NE>น.ส.</NEอ้อ</NE>', '<NE>น.ส.อ้อ</NE>'),
         ('<NE>AB>พล.อ.เปรม ติณสูลานนท์</NE>',
          '<NE><AB>พล.อ.</AB>เปรม ติณสูลานนท์</NE>'),
         ('<NE>AB>อ.แว้ง</NE>', '<NE><AB>อ.</AB>แว้ง</NE>'),
         ('<NE>หจก.AB>สสวท.</NE>', '<NE>หจก.<AB>สสวท.</AB></NE>'),
         ('<NE>สหภาพแรงงานรัฐวิสาหกิจบริษัท อสมท จำกัด(มหาชน)</NE</NE>>',
          '<NE>สหภาพแรงงานรัฐวิสาหกิจบริษัท อสมท จำกัด(มหาชน)</NE>'),
         ('<NEพี่มน</NE>', '<NE>พี่มน</NE>'),
         ('<NE>MERGE>เมืองไทย</NE>', '<NE>เมืองไทย</NE>')]


class Denoiser(object):
    @classmethod
    def run(cls, data):
        ddata = []
        for l in data:
            for case in CASES:
                if case[0] in l:
                    l = l.replace(case[0], case[1])
            ddata.append(l)
        return ddata
