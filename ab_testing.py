####AB Testi ile Bidding Yöntemlerinin Dönüşümünün Karşılaştırılması#####

##İş Problemi##
#Facebook kısa süre önce mevcut "maximum bidding" adı verilen teklif verme türüne alternatif olarak yeni bir teklif türü olan "average bidding"’i tanıttı.
#Müşterilerimizden biri olan bombabomba.com, bu yeni özelliği test etmeye karar verdi ve average bidding'in maximum bidding'den daha fazla dönüşüm getirip
#getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz
#etmenizi bekliyor. Bombabomba.com için nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchase metriğine odaklanılmalıdır.

#Veri Seti Hikayesi
#Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları reklam sayıları gibi bilgilerin yanı sıra buradan gelen
#kazanç bilgileri yer almaktadır. Kontrol ve Test grubu olmak üzere iki ayrı veri seti vardır.
#Bu veri setleri ab_testing.xlsx excel’inin ayrı sayfalarında yer almaktadır. Kontrol grubuna Maximum Bidding, test grubuna Average Bidding uygulanmıştır.

import pandas as pd
from scipy.stats import shapiro, levene, ttest_ind
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pd.set_option("display.float_format", lambda x: "%.5f" % x)

#Görev 1: Veriyi Hazırlama ve Analiz Etme
#Adım 1: ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.
df_control = pd.read_excel("ab_testing.xlsx", sheet_name="Control Group")
df_test = pd.read_excel("ab_testing.xlsx", sheet_name="Test Group")

#Adım 2: Kontrol ve test grubu verilerini analiz ediniz.
def df_check(dataframe, head=5):
    print("###### Shape ######")
    print(dataframe.shape)
    print("###### Head ######")
    print(dataframe.head(head))
    print("###### Dtpes ######")
    print(dataframe.dtypes)
    print("###### NA ######")
    print(dataframe.isnull().sum())

df_check(df_control)
df_check(df_test)

#Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.
df_control["Group"] = "control"
df_test["Group"] = "test"
df = pd.concat([df_control, df_test], axis=0, ignore_index=True)
df.head()

#Görev 2: A/B Testinin Hipotezinin Tanımlanması
#Adım 1: Hipotezi tanımlayınız.
#H0 : M1 = M2 (Kontrol grubu ve test grubu satın almaları arasında fark yoktur.)
#H1 : M1!= M2 (Kontrol grubu ve test grubu satın almaları arasında fark vardır.)

#Adım 2: Kontrol ve test grubu için purchase (kazanç) ortalamalarını analiz ediniz.
df.groupby("Group").agg({"Purchase": "mean"})

#Görev 3: Hipotez Testinin Gerçekleştirilmesi
#Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.

#Normallik Varsayımı :
test_value, p_value = shapiro(df.loc[df["Group"] == "control", "Purchase"])
print("Test_value = %.5f, p_value = %.5f" % (test_value, p_value))
#pvalue > 0.05 H0 reddedilemez.Normallik sağlanmıştır
test_value, p_value = shapiro(df.loc[df["Group"] == "test", "Purchase"])
print("Test_value = %.5f, p_value = %.5f" % (test_value, p_value))
##pvalue > 0.05 H0 reddedilemez.Normallik sağlanmıştır

#Varyans Homojenliği :
test_value, p_value = levene(df.loc[df["Group"] == "control", "Purchase"],
                             df.loc[df["Group"] == "test", "Purchase"])
print("test_value = %.5f, p_value = %.5f" % (test_value, p_value))
#pvalue > 0.05 H0 reddilemez.Homojenlik sağlanmıştır.

#Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz.
#Parametrik iki örneklem T testi uygundur.
test_value, p_value = ttest_ind(df.loc[df["Group"] == "control", "Purchase"],
                                df.loc[df["Group"] == "test", "Purchase"],
                                equal_var=True)
print("test_value = %.5f, p_value = %.5f" % (test_value, p_value))

#Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.
#p_value = 0.34933 olarak bulunmuş olup 0.05ten büyük olduğu için H0 hipotezi reddedilememiştir.Yani kontrol ve test grubu satın alma ortalamaları arasında anlamlı bir fark yokturç

#Görev 4: Sonuçların Analizi
#Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.
#Hipotzler kurrulduktan sonra normallik varsayımı ve varyans homojenliği varsayımına bakılmış olup her iki var sayım da reddedilemeiştir.Bu varsayımlar sağlandığı için
#İki örneklem bağımsız T Testi uygulanmış olup p value değeri 0.05'ten büyük bir değer elde edilmiştir.Bu değer ışığında H0 hipotezi reddedilememiştir.

#Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.
#Satın alma açısından anlamlı bir fark yoktur.İki yöntemden biri seçilebilir ya da diğer değişkenlerdeki farklılıklar değerlendirilebilir.Gözlemleye devam edilebilir.

