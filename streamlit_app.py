import streamlit as st
import pandas as pd

st.title(":blue[Konut Birikimi]")
st.markdown("***Burada çeşitli parametrelerle daire(ler) alabilme ihtimallerinizi değerlendirebileceksiniz...***")
st.text("")
#with st.sidebar:
    #st.write("")
with st.container():
    with st.container(border=True):
        yas1=st.slider("**Yaş aralığını seçiniz..**", 0,130,(25,65))
        st.caption(f"*{str(yas1[0])}-{str(yas1[1])} yaş aralığı içerisinde daire(ler) almayı planlıyorsunuz.*")
    toplamay=int((yas1[1]-yas1[0])*12)
    suankiay=1

    with st.container(border=True):
        col1,col2=st.columns(2)
        with col1:
            toplananpara = st.number_input("**Sermayeniz(₺):**", value=0,step=100000)
        with col2:
            aylik = st.number_input("**Aylık gerliriniz(₺):**", value=3000, step=1000)

        col3,col4=st.columns(2,border=False,vertical_alignment="bottom")
        with col3:
            kira = st.number_input("**Daire(ler) için beklenen kira geliri(₺):**", value=8000,step=1000)
        with col4:
            if toplananpara == 0:
                st.caption(f"***Hiç paranız yok** ve aylık geliriniz **{str(aylik)} ₺,***")
            elif toplananpara < 0:
                st.caption(f"***{str(abs(toplananpara))} ₺** borcunuz var ve aylık geliriniz **{str(aylik)} ₺,***")
            else:
                st.caption(f"***{str(toplananpara)} ₺** paranız var ve aylık geliriniz **{str(aylik)} ₺,***")
            st.caption(f"*Beklenen kira geliri ise **{kira}₺'dir.***")
        st.caption("---")

        col5, col6 = st.columns(2)
        with col5:
            evfiyat = st.number_input("**Varsayılan daire fiyatı(₺):**", value=1250000,step=50000)
        with col6:
            pesinatyuzdesi = st.slider("**Peşinat yüzdesini seçiniz:**", 0, 100, 20)
        pesinat = evfiyat * pesinatyuzdesi / 100
        st.caption(f"*{format(evfiyat,',')} ₺ değerindeki daire için **{format(int(pesinat),',')} ₺** peşinat vermeniz gerekiyor.*")
        st.caption("---")

        col7,col8=st.columns([3,1])
        with col7:
            kredi = st.number_input("**Kredi süresini seçiniz:**", value=15)
        with col8:
            ayyil = st.segmented_control("", options=["Yıl","Ay"],selection_mode="single",default="Yıl")
        if ayyil == "Yıl":
            krediay = kredi*12
            krediyil=kredi
        else:
            krediay=kredi
            krediyil=round(kredi/12,1)
        gider = (evfiyat - pesinat) / krediay
        st.caption(f"*{str(krediyil)} yıl ({krediay} ay) sürecek krediniz için, aylık **{round(gider)} ₺** ödemeniz gerekiyor.*")
        st.caption("")

evsayisi=0
listeborcay=[]
aylik0=aylik
krediborcu=0 #toplam kredi borcumuz
netgelirls=[]
sermayels=[]
krediborcls=[]
#zamanyasls=[]
zamanls=[]
aktifkredisayisils=[]
evsayisils=[]

for i in range(suankiay,toplamay+1):
    gidersayisi = 0
    for t2 in listeborcay:
        if t2 > 0:
            gidersayisi += 1
    toplananpara -= gidersayisi * gider
    toplananpara+=aylik
    krediborcu-=gidersayisi*gider #aylık toplam kredi borcumuz
    netgelir00=aylik-(gidersayisi*gider) #aylık net gelirimiz
    clist=[]
    for t3 in listeborcay:
        clist.append(t3-1)
    listeborcay=clist
    while True:
        if toplananpara>=pesinat:
            toplananpara-=pesinat
            evsayisi+=1
            listeborcay.append(krediay)
            aylik=aylik+kira
            krediborcu+=(evfiyat-pesinat)
        else:
            break
    aktifkredisayisi=0 #aylık net aktif kredi sayımız için ekledik, gider sayısından farklı orada ödeme yapılıyor, burada borç olarak ekleniyor.
    for t2 in listeborcay:
        if t2 > 0:
            aktifkredisayisi += 1
    yil=i//12 #anlıkyıl, i anlık ay.
    yilinayi=i%12
    if yilinayi==0: #ay ve yıl gösteriminde düzeltmeler
        yilinayi=12
        yil-=1
    yilinayi = "{:02d}".format(yilinayi)
    yasyili = yas1[0] + yil
    #zamanyasls.append(yasyili)
    zamanls.append(f"{yasyili}-{yilinayi}")
    netgelirls.append(netgelir00)
    sermayels.append(toplananpara)
    krediborcls.append(krediborcu)
    aktifkredisayisils.append(aktifkredisayisi)
    evsayisils.append(evsayisi)
    suankiay+=1

suankiay-=1
gidertop=gidersayisi*gider
suankiyil=suankiay//12
kiragelir=evsayisi*kira
data={
    "Zaman":zamanls,
    "Net gelir":netgelirls,
    "Sermaye":sermayels,
    "Kredi borç yükü":krediborcls,
    "Devam eden kredi sayısı":aktifkredisayisils,
    "Toplam daire sayısı":evsayisils
    }
df=pd.DataFrame(data)
df=df.sort_values("Zaman")
btn=st.button("Sonuç için tıklayınız")
if btn:
    st.caption(f"Sermaye: ***{format(round(toplananpara))}₺***")
    st.caption(f"Aylık gelir: ***{str(round(aylik))}₺***(Kira getirisi: {str(round(aylik-aylik0))}₺) - Aylık gider: ***{str(round(gidertop))}₺*** = Net gelir: ***{str(round(aylik-gidertop))}₺***")
    st.caption(f"Aktif kredi sayısı: ***{str(gidersayisi)}***")
    st.caption(f"Daire sayısı: ***{str(evsayisi)}***")
    st.dataframe(df)

code="""import streamlit as st
import pandas as pd

st.title(":blue[Konut Birikimi]")
st.markdown("***Burada çeşitli parametrelerle daire(ler) alabilme ihtimallerinizi değerlendirebileceksiniz...***")
st.text("")
#with st.sidebar:
    #st.write("")
with st.container():
    with st.container(border=True):
        yas1=st.slider("**Yaş aralığını seçiniz..**", 0,130,(25,65))
        st.caption(f"*{str(yas1[0])}-{str(yas1[1])} yaş aralığı içerisinde daire(ler) almayı planlıyorsunuz.*")
    toplamay=int((yas1[1]-yas1[0])*12)
    suankiay=1

    with st.container(border=True):
        col1,col2=st.columns(2)
        with col1:
            toplananpara = st.number_input("**Sermayeniz(₺):**", value=0,step=100000)
        with col2:
            aylik = st.number_input("**Aylık gerliriniz(₺):**", value=3000, step=1000)

        col3,col4=st.columns(2,border=False,vertical_alignment="bottom")
        with col3:
            kira = st.number_input("**Daire(ler) için beklenen kira geliri(₺):**", value=8000,step=1000)
        with col4:
            if toplananpara == 0:
                st.caption(f"***Hiç paranız yok** ve aylık geliriniz **{str(aylik)} ₺,***")
            elif toplananpara < 0:
                st.caption(f"***{str(abs(toplananpara))} ₺** borcunuz var ve aylık geliriniz **{str(aylik)} ₺,***")
            else:
                st.caption(f"***{str(toplananpara)} ₺** paranız var ve aylık geliriniz **{str(aylik)} ₺,***")
            st.caption(f"*Beklenen kira geliri ise **{kira}₺'dir.***")
        st.caption("---")

        col5, col6 = st.columns(2)
        with col5:
            evfiyat = st.number_input("**Varsayılan daire fiyatı(₺):**", value=1250000,step=50000)
        with col6:
            pesinatyuzdesi = st.slider("**Peşinat yüzdesini seçiniz:**", 0, 100, 20)
        pesinat = evfiyat * pesinatyuzdesi / 100
        st.caption(f"*{format(evfiyat,',')} ₺ değerindeki daire için **{format(int(pesinat),',')} ₺** peşinat vermeniz gerekiyor.*")
        st.caption("---")

        col7,col8=st.columns([3,1])
        with col7:
            kredi = st.number_input("**Kredi süresini seçiniz:**", value=15)
        with col8:
            ayyil = st.segmented_control("", options=["Yıl","Ay"],selection_mode="single",default="Yıl")
        if ayyil == "Yıl":
            krediay = kredi*12
            krediyil=kredi
        else:
            krediay=kredi
            krediyil=round(kredi/12,1)
        gider = (evfiyat - pesinat) / krediay
        st.caption(f"*{str(krediyil)} yıl ({krediay} ay) sürecek krediniz için, aylık **{round(gider)} ₺** ödemeniz gerekiyor.*")
        st.caption("")

evsayisi=0
listeborcay=[]
aylik0=aylik
krediborcu=0 #toplam kredi borcumuz
netgelirls=[]
sermayels=[]
krediborcls=[]
#zamanyasls=[]
zamanls=[]
aktifkredisayisils=[]
evsayisils=[]

for i in range(suankiay,toplamay+1):
    gidersayisi = 0
    for t2 in listeborcay:
        if t2 > 0:
            gidersayisi += 1
    toplananpara -= gidersayisi * gider
    toplananpara+=aylik
    krediborcu-=gidersayisi*gider #aylık toplam kredi borcumuz
    netgelir00=aylik-(gidersayisi*gider) #aylık net gelirimiz
    clist=[]
    for t3 in listeborcay:
        clist.append(t3-1)
    listeborcay=clist
    if toplananpara>=pesinat:
        toplananpara-=pesinat
        evsayisi+=1
        listeborcay.append(krediay)
        aylik=aylik+kira
        krediborcu+=(evfiyat-pesinat)
    aktifkredisayisi=0 #aylık net aktif kredi sayımız için ekledik, gider sayısından farklı orada ödeme yapılıyor, burada borç olarak ekleniyor.
    for t2 in listeborcay:
        if t2 > 0:
            aktifkredisayisi += 1
    yil=i//12 #anlıkyıl, i anlık ay.
    yilinayi=i%12
    if yilinayi==0: #ay ve yıl gösteriminde düzeltmeler
        yilinayi=12
        yil-=1
    yilinayi = "{:02d}".format(yilinayi)
    yasyili = yas1[0] + yil
    #zamanyasls.append(yasyili)
    zamanls.append(f"{yasyili}-{yilinayi}")
    netgelirls.append(netgelir00)
    sermayels.append(toplananpara)
    krediborcls.append(krediborcu)
    aktifkredisayisils.append(aktifkredisayisi)
    evsayisils.append(evsayisi)
    suankiay+=1

suankiay-=1
gidertop=gidersayisi*gider
suankiyil=suankiay//12
kiragelir=evsayisi*kira
data={
    "Zaman":zamanls,
    "Net gelir":netgelirls,
    "Sermaye":sermayels,
    "Kredi borç yükü":krediborcls,
    "Devam eden kredi sayısı":aktifkredisayisils,
    "Toplam daire sayısı":evsayisils
    }
df=pd.DataFrame(data)
df=df.sort_values("Zaman")
btn=st.button("sonuç")
if btn:
    st.caption(f"Sermaye: ***{format(round(toplananpara))}₺***")
    st.caption(f"Aylık gelir: ***{str(round(aylik))}₺***(Kira getirisi: {str(round(aylik-aylik0))}₺) - Aylık gider: ***{str(round(gidertop))}₺*** = Net gelir: ***{str(round(aylik-gidertop))}₺***")
    st.caption(f"Aktif kredi sayısı: ***{str(gidersayisi)}***")
    st.caption(f"Daire sayısı: ***{str(evsayisi)}***")
    st.dataframe(df)"""

with st.expander("Codes:"):
    st.code(code, language="python")

