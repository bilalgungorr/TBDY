"""
Bu kod TBDY-2018'de yer alan 'Tablo 3.4. Deprem Tasarım Sınıflarına Gore 
Yeni Yapılacak veya Mevcut Binalar İcin Performans Hedefleri ve Uygulanacak
Degerlendirme/Tasarım Yaklasımları' baslikli tablodan ilgili performans hedefi
ve degerlendirme/tasarim yaklasimlari ikilisi asagidaki bilgileri hesaplayarak
bulur.
    1. Deprem tasarim siniflari
    2. Bina yukseklik siniflari
"""

__author__ = 'bilalgungorr'


def findDTS(SDS, BKS):
    """
    Deprem tasarim sinifini bulur (str).
    Parametreler:
        SDS: DD-2 Deprem yer hareketi duzeyindeki kisa periyot tasarim
        spektral ivme katsayisi.
        BKS (int): Bina kullanim sinifi.
    """
    
    if SDS < 0.33:
        dts = '4'
    elif SDS >= 0.75:
        dts = '1'
    elif 0.33 <= SDS < 0.5:
        dts = '3'
    elif 0.5 <= SDS < 0.75:
        dts = '2'

    return dts + (BKS==1)*'a'

def findBYS(HN, DTS):
    """
    Bina yukseklik sinifini bulur. 
    Parametreler:
        HN (float): Bina yuksekligi.
        DTS (str): Deprem tasarim sinifi.
    """

    BYS_list = [70, 56, 42, 28, 17.5, 10.5, 7]

    if DTS in ['3', '3a']:
        BYS_list = [91, *BYS_list[:-1]]

    elif DTS in ['4', '4a']:
        BYS_list = [105, 91, BYS_list[1:-1]]

    lenb = len(BYS_list)

    if HN > BYS_list[0]:
        return 1

    if HN <= BYS_list[-1]:
        return 8

    for i in range(lenb - 1):
        if BYS_list[i+1] < HN <= BYS_list[i]:
            return i + 2 


Table3_4= dict(
    a1 = dict(
        DD2 = ['KH', 'DGT']),
    a2 = dict(
        DD3 = ['SH', 'SGDT'],
        DD2 = ['KH', 'DGT'],
        DD1 = ['KH', 'SGDT']),

    b1 = dict(
        DD4 = ['KK', 'DGT'],
        DD2 = ['KH', 'DGT'],
        DD1 = ['GO', 'SGDT']),
    b2 = dict(
        DD3 = ['SH', 'SGDT'],
        DD2 = ['KH', 'DGT'],
        DD1 = ['KH', 'SGDT']),

    c1 = dict(
        DD2 = ['KH', 'SGDT']),
    c2 = dict(
        DD3 = ['SH', 'SGDT'],
        DD1 = ['KH', 'SGDT'])
)



def findGroup(yapi_durumu, DTS, BYS):
    """
    Yonetmelikteki Tablo 3.4'de bulunan alt tablo grubunu bulur.
    Parametreler:
        yapi_durumu(str): {'yeni', 'mevcut'}
            yeni: Yeni Yapılacak Yerinde Dökme Betonarme, 
                Önüretimli Betonarme ve Çelik Binalar 
            mevcut: Mevcut Yerinde Dökme Betonarme, 
                Önüretimli Betonarme ve Çelik Binalar 
        DTS (str): Deprem tasarim sinifi.
        BYS: (int): Bina yukseklik sinifi.
    """

    dts_group = ['1a', '2a'] 
  
    # Yuksek binalar, BYS = 1 
    if BYS == 1:
        return 'b' + str(1 + (DTS in dts_group))

    # mevcut binalar, BYS >= 2 
    if yapi_durumu == 'mevcut':
        return 'c' + str(1 + (DTS in dts_group))

    # yeni binalar, BYS >= 2
    if yapi_durumu == 'yeni':
        return  'a' + str(1 + (DTS in dts_group and BYS <= 3))


def findPH(SDS, BKS, HN, yapi_durumu, DD=-1):
    """
    Parametreler:
        SDS: DD-2 Deprem yer hareketi duzeyindeki kisa periyot tasarim
        spektral ivme katsayisi.
        BKS (int): {1, 2, 3} Bina kullanim sinifi.
        HN (float): Bina yuksekligi.
        yapi_durumu (str): {'yeni', 'mevcut'}
            yeni: Yeni Yapılacak Yerinde Dökme Betonarme, 
                Önüretimli Betonarme ve Çelik Binalar 
            mevcut: Mevcut Yerinde Dökme Betonarme, 
                Önüretimli Betonarme ve Çelik Binalar 
        DD (int): {1, 2, 3, 4} Deprem yer hareketi duzeyi.
            DD -1 ise tum deprem duzeylerine iliskin bilgiyi geri donderir.
    """
    
    DD = 'DD' + str(DD)
    DTS = findDTS(SDS, BKS)
    BYS = findBYS(HN, DTS)
    print(f'Deprem tasarim sinif: {DTS}, Bina yukseklik sinifi: {BYS}') 
    group = findGroup(yapi_durumu, DTS, BYS)
    
    Notes = ['Not: On tasarim olarak yapilacaktir.',
             'Not: I = 1.5 alinarak uygulanacaktir.',
             'Not: Bolum 8’de tanimlanan tam ard-germeli onuretimli binalarin\
    on tasarimi DGT yaklasimi ile, kesin tasarimi ise 8.4.3’e gore\
    SGDT yaklasimi ile yapilacaktir.']
   
    if DD in ['DD2', -1]:
        if group == ['a2', 'b1', 'b2']:
            print(Notes[0])

        if group in ['a2', 'b2']:
            print(Notes[1])

        if group == 'a1':
            print(Notes[2])
        
    if DD == -1:
        print('Notlar deprem yer hareketi duzeyinin DD-2 olmasi durumundadir')
        return Table3_4[group]
    result = Table3_4[group].get(DD)
    if not result:
        print('Gecerli deprem duzeyleri:' + ', '.join(Table3_4[group].keys()))
    else:
        return result

if __name__ == '__main__':
    ph = findPH(0.5, 1, 50, 'yeni', DD=2)
    print(ph)

