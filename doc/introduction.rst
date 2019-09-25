What is DHT?
^^^^^^^^^^^^

在解釋Kademlia前先說說DHT的概念，DHT為\ **distributed hash
table**\ (分散式雜湊表)的縮寫，概念上來說，每筆**data**\ 都有對應的\ **key**\ ，只要給定\ **key**\ 就能從網路上取得\ **data**\ 。

.. figure:: https://zh.wikipedia.org/wiki/%E5%88%86%E6%95%A3%E5%BC%8F%E9%9B%9C%E6%B9%8A%E8%A1%A8#/media/File:DHT_en.svg,%20圖片引用自wiki
   :alt: 

應用在這專案中(P2PLending)來解釋，只要有ID，就能找到對應的借貸資料，或是另一位peer

What is Kademlia?
^^^^^^^^^^^^^^^^^

Kademlia是一種DHT演算法，將peer與檔案視為同構，也就是說檔案ID與peer
ID可以相同，而演萬法上也會把檔案存在相同ID的peer上。

How Kademlia work?
^^^^^^^^^^^^^^^^^^

Kademlia將整個系統映射至二元樹上，所有ID都是一組只有0或1的bit字串，0為左子樹，1為右子樹。以下先解釋幾個概念

XOR距離運算
'''''''''''

任意兩ID進行XOR運算結果定義為彼此的距離

Kbucket
'''''''

對於任何一個節點來說，由root開始算，將\ **不包含**\ 自己的子樹劃分出來即為一個Kbucket，\ **K**\ 代表這bucket最多會存著\ **K**\ 個節點。只要所有Kbucket都至少存有一個節點，該節點就可以遍歷整個網路

.. figure:: https://en.wikipedia.org/wiki/Kademlia#/media/File:Dht_example_SVG.svg,%20圖片引用自wiki
   :alt: 

路由機制
''''''''

| 為甚麼這樣就能遍歷網路？
| 由於Kbucket是拆分出來的子樹，同bucket內的節點前綴會相同，當今天把資料送給某個位置未知的節點X時，只要把資料交給同Kbucket內的節點Y，這樣等於把距離收斂至bucket內，節點Y再以自己的視角找尋bucket內的其他節點，就能將距離收斂至找到目標。

.. figure:: https://lh6.googleusercontent.com/J9ebpRdPW788CCFetj0KJhS4mTwHGeOwppibQ2-dBuwlMWjQoKdPi5VBbWMJpI_04XYvULA3Hm4kGIQF15RSFOWkq_qI4U93V39eDHrM3lxemgESNJ8JogVIBjjGNt3EXs-141V0GBg,%20圖片引用自https://program-think.blogspot.com/2017/09/Introduction-DHT-Kademlia-Chord.html
   :alt: 

Getting start
^^^^^^^^^^^^^

Kademlia initial
''''''''''''''''

自己一人是無法構成網路的，想要拓展自己的網路就要先update一個已知節點的資料，向對方發出GET
node
SelfID請求，也就是請對方找\ **自己**\ ，Kademlia節點只要收到任何請求都會先將對方update進自己的bucket然後才執行其他動作，當收到GET
node
SelfID的請求時，對方就會將自己加入bucket中，然後回傳對方bucket中離自己最近的其他節點，再向這些節點發出請求，如此遞迴下去，就能完備自己的bucket資料

update
''''''

跟新一個節點到自己的bucket內，如果bucket已到達上限\ **K**\ ，就會檢查最舊的節點有無響應(ping他)，如果有，就把該節點移到最前面(視為最新)，並捨棄新加入的節點，否則就刪除舊節點加入新節點。

LookUp
''''''

當執行LookUp會看自己的bucket內有無該節點，有就直接回傳，否則會開始依參數\ **a**\ 分\ **a**\ 個thread下去調度同bucket內的其他節點發出GET
node請求，其他節點收到請求後，如果自己存有該節點資料就會直接回傳，否則會回傳\ **K**\ 個最接近的節點

UpLoad
''''''

DownLoad
''''''''
