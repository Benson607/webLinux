# 何以為此案
此案乃為以終端為形之linux，創其程式之案，亦有C/C++、python、java之案，以無複之、無貼之、無輔之，亦非便也，而欲創此案；
乃以https之形，而以python為根，所創之服務也；
亦為網，而為頁也，嚴以曰之，亦可稱其為網頁；
以MonacoEditor庫為其輔，輔生複，有複之亦有貼之，亦為便也；

# 何以喚此案
此案乃存於github之上，亦可運以git，對其萬物連結之中，所在之處，行以clone，亦複於天，流傳於天地之間，而貼於地也；

    git clone git@github.com:Benson607/webLinux.git

# 何以行此案
欲行此案，必對此案所賴之基底，安之，裝之；
此案亦賴於二，python3.8，一也，Flask，二也；

其一，原對python3.8，亦有運以apt，行以install，曰其名python3.8之法，天聞之而應也；

    sudo apt install python3.8

而自ubuntu20.04之後，python之中，亦有二也、亦有三也；
天地見之，乃聞風喪膽，始，天聞三者，應也，非三者，天聞而不應，若為三者，而以一點，接以一數，指其3.X，天亦不應也；
而天地之間，亦有應者，始之ubuntu20.04，爾後亦自有python3也；

其二，亦簡，運以pip，行以install，曰其名Flask，天應；

    pip install Flask

待其賴者立於爾等之地，仍需創公、私鑰，為其https所用；
運以openssl，請以req，欽以x509之證，示newkey為新鑰，且以rsa2048為其秘法，指其keyout為key.pem，再指其out為cert.pem，宣以days，示其消亡之日，為一春夏秋冬；行之；

    openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365

待爾等之地中，現以key.pem、cert.pem，則其鑰樹之；
運以bash，行以start.sh；

    bash start.sh

此案運之；

若欲止此案；則運以bash，行以stop.sh；

    bash stop.sh

案止；