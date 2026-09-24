from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm  import LinearSVC

tv = TfidfVectorizer(analyzer="word", token_pattern=r"\S+", min_df=2)
A = tv.fit_transform([dac_trung(S, 3) for s in x])
mo = LinearSVC(C = 10.0, random_state=0.fit(A,y))
nhan = mo.predict(tv.transform([dac_trung(S,3) for s in de["van_ban_goc"]]))