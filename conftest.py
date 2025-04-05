import warnings

"""
 DeprecationWarning: 'crypt' is deprecated and slated for removal in Python 3.13
    from crypt import crypt as _crypt
 
 파이썬 3.13으로 버전 올리면 passlib 관련 되어서 문제 생김.
 지금은 3.12라서 워닝만 뜨는데. 해당 내용 제거
"""
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module=r"passlib\.utils"
)
