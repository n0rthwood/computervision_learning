function [BW,maskedImage] = segmentImageGrab(X)
%segmentImage Segment image using auto-generated code from imageSegmenter app
%  [BW,MASKEDIMAGE] = segmentImage(X) segments image X using auto-generated
%  code from the imageSegmenter app. The final segmentation is returned in
%  BW, and a masked image is returned in MASKEDIMAGE.

% Auto-generated by imageSegmenter app on 09-Jul-2022
%----------------------------------------------------


% 图割
foregroundInd = [137641 137643 139481 141321 142239 144079 144999 148679 149599 153279 153515 154199 157878 158115 160638 160875 162478 163635 165238 167076 167315 169836 170075 171676 172594 172596 172835 174008 174434 175848 176273 176274 176768 177191 177193 177435 179031 179275 180871 181791 182035 183631 183875 185471 383736 384656 386496 386498 388338 389258 391099 392939 393633 394553 395701 396393 397543 398233 398463 399153 400993 401224 401913 403066 403753 404906 405102 405828 406024 406025 406513 407865 407867 408353 409508 409709 409710 409767 410428 410632 410634 410635 410637 410640 410643 410645 410647 410650 410652 410653 410655 410657 410658 410660 410662 410663 410665 410667 410668 410672 410673 410677 410678 410680 410682 410683 410685 410687 411113 414109 414111 414793 415031 415713 417553 420313 422153 423993 426753 428593 429513 431353 433193 434113 435953 437793 438713 440553 442393 443313 445153 446993 447913 602020 603860 606620 609382 613063 615823 618583 622263 625025 627556 627785 629625 634225 635834 636985 640667 641587 643427 645034 645267 646187 648027 649634 649867 650787 652394 652627 653547 653756 655387 655596 656994 657227 657436 658147 659754 659987 660194 661827 662747 662954 664353 664587 664794 666427 667113 667347 667554 669187 670793 671027 672154 673553 673787 673994 675627 676313 678151 678594 680911 682751 683194 685511 687794 689189 689191 690554 691949 693789 694234 694708 694709 696548 696994 698388 698834 699306 699308 701146 702986 703906 876866 878706 879626 884226 890668 895268 898028 904468 909069 914589 919191 923791 925631 928391 932991 932993 934833 1126631 1127113 1127551 1128953 1129389 1131229 1133553 1133989 1138589 1139993 1140429 1142753 1142973 1143189 1145511 1145949 1147351 1149629 1151951 1154229 1154711 1156773 1156988 1156989 1158613 1159311 1159533 1162071 1162293 1162508 1164133 1164348 1165751 1168509 1168948 1170349 1170788 1171269 1171708 1173109 1174949 1355492 1356412 1358252 1364690 1367450 1370210 1376650 1379410 1383090 1385850 1386081 1387690 1390450 1393210 1395050 1395281 1396890 1397810 1398041 1399648 1401488 1401721 1402408 1404248 1404481 1409081 1410921 1411841 1413681 1418281 1419201 1422883 1423803 1425643 1427483 1428403 1430243 ];
backgroundInd = [76408 83768 88366 90206 92966 95726 99406 102166 104926 108606 113206 115966 118726 123326 127006 129766 132526 137126 140806 143566 148166 152766 155526 160126 162886 166566 172086 175766 178526 183126 185886 190486 194166 195086 198766 203366 208886 212566 217166 222686 229126 233726 235256 238326 242926 243536 247526 248136 250286 250896 253046 255496 256726 259486 260097 264086 266537 266846 270526 271139 273286 276046 276659 279726 280646 281261 285246 287086 289541 289846 291685 294445 295061 296285 298125 299045 300885 302725 303342 303643 304262 307323 308243 310083 311923 312843 313462 314683 315603 317443 319281 320201 322041 323881 324801 325422 326641 329401 331241 333081 335841 337680 338304 338600 342280 343200 345040 347800 349638 349640 350264 352398 354238 356998 358838 360678 361596 364064 365276 366196 369876 370796 373264 374476 375396 377235 379075 381835 383675 385224 386435 387064 389195 391035 391664 392875 395633 398393 401153 401784 402993 404833 407593 408224 410351 412191 414031 414664 414951 415584 416791 419551 420184 423231 424151 426624 427831 430591 431224 432431 435191 437031 437664 439791 440424 442550 444390 446864 447150 448990 449624 451750 453590 455430 456350 456984 458190 460664 460950 461584 464630 465550 469230 469864 470150 473831 474464 476591 478431 479351 481191 481824 483031 483951 485791 486424 486711 488551 490391 491310 491311 493150 493784 500224 507584 512184 514241 518624 521384 527826 528041 530586 530801 535186 535401 539786 540001 544386 544603 550826 551043 553586 556563 558186 560946 561163 562786 567386 569443 570146 574746 576586 576803 578718 579346 582323 583946 585786 586078 586706 586923 589758 590386 590678 591306 593146 593363 594360 594986 595906 597746 598960 599586 599803 600506 602346 604186 604480 605106 605323 606946 608786 609081 609706 609923 611546 613386 615521 616365 620121 622805 623725 626563 630165 633923 639365 645886 648565 657765 657846 667885 668888 677085 679928 686285 693728 699165 699646 705689 706085 706525 710685 713445 715285 717344 717563 717649 718043 722643 726323 728691 729302 729523 733683 736051 738283 740834 741043 741483 743102 745251 748403 748622 752611 754634 755062 755281 756681 759051 759441 761281 761502 763651 765881 766321 768251 768434 768862 770480 771011 773034 773240 774691 774874 775080 775302 776000 776222 777451 778281 779291 779474 779680 782051 782440 783891 784502 784811 784994 785198 786651 788491 788878 789411 789594 790022 791251 791636 793091 794009 794396 795849 796034 796462 798609 798996 800449 800836 801281 802289 803209 803824 805436 806889 807074 807809 808196 808424 809649 811489 812594 812796 813024 814249 814636 816920 817009 817624 819034 820689 821076 823449 824369 824756 826394 826824 828969 831196 831424 832649 832834 835409 835796 836024 838078 838169 838354 840624 841849 842236 843384 844609 844794 844996 845224 849209 849596 849824 851049 851232 852584 854196 854638 855649 856264 856569 856956 858592 859026 860248 860636 861786 863008 863192 864848 865236 865466 867608 867996 868226 869448 870552 870756 871198 872206 872826 874046 875356 875586 876806 876992 878646 879036 879566 880186 881406 881592 881796 883246 884166 884556 884786 886005 887845 888032 888765 888951 889156 889386 889596 890603 892443 892836 893066 893363 895201 895391 895596 897041 897961 898586 899801 900196 901640 901831 902266 902476 902560 902956 904400 906238 906636 906866 907351 907556 908998 910546 911758 912156 913791 913996 914226 914516 915356 916756 918196 919516 919746 920955 921149 921356 923715 924116 924346 924556 925749 927395 927796 928026 930153 930556 931993 932189 932396 932626 932836 934753 935156 937226 937511 937916 939351 939549 939756 939986 942111 942516 942746 942956 943951 944147 944356 945791 946196 946426 946710 947116 948956 949186 950390 950587 950796 951236 951310 951507 951716 953150 953556 953786 954990 955396 956107 956316 956546 957750 958156 958596 959996 960510 960706 960916 961146 962350 962756 964190 964596 964826 965306 965516 965956 966950 967356 968790 968986 969196 969426 970116 971550 971956 972186 973390 973586 973796 974236 974310 974506 974716 974946 976150 976556 977990 978186 978396 978910 979316 979546 979756 980750 980946 981156 982996 983510 983706 983916 984146 985350 985546 985756 985986 986196 987190 987386 987596 988110 988516 990146 990358 990586 991790 992198 992710 992906 993118 993346 993556 994746 995666 995878 996104 997310 997718 998155 999150 999346 999558 999784 1000266 1000478 1001910 1002318 1002544 1003946 1004158 1004595 1004670 1004864 1005078 1005304 1006918 1008350 1008544 1008758 1008984 1009195 1009270 1009464 1009678 1009904 1011518 1012950 1013144 1013358 1013584 1013795 1014064 1014278 1015710 1016118 1017958 1018184 1018393 1018470 1018664 1018878 1019104 1019313 1020504 1020718 1020720 1022150 1022560 1022784 1023264 1023480 1024910 1025320 1025544 1026944 1027160 1027593 1027671 1028080 1028304 1029704 1029920 1030353 1031760 1031984 1032271 1032464 1032680 1032904 1034111 1034520 1034953 1036360 1036584 1037064 1037280 1037713 1038711 1039121 1039344 1040744 1040961 1041184 1041393 1041471 1041881 1043504 1043944 1045561 1045993 1046071 1046264 1046481 1046702 1048321 1049751 1049942 1050161 1050163 1050382 1050593 1051083 1051302 1052702 1052923 1053142 1053353 1054763 1055271 1055462 1055683 1055902 1056113 1057302 1057523 1057742 1059363 1059792 1059871 1060062 1060502 1061902 1062123 1062342 1063963 1064392 1064471 1064662 1064883 1065102 1066502 1066725 1066942 1067152 1068565 1068782 1069073 1069262 1069485 1069912 1071102 1071325 1071542 1072942 1073673 1074085 1074302 1074512 1075702 1075925 1076142 1076352 1076845 1078273 1078462 1078685 1078902 1079112 1080302 1080525 1080742 1081033 1081222 1081445 1081662 1081872 1083062 1083285 1083502 1084901 1085126 1085342 1085552 1085821 1086046 1086262 1087473 1087661 1087886 1088102 1088312 1089726 1090646 1092073 1092486 1092912 1094326 1095246 1095672 1096673 1097086 1098926 1099352 1099846 1101688 1103113 1103528 1103952 1104448 1105873 1106288 1108128 1108552 1109048 1110473 1110888 1111312 1112728 1113648 1115073 1115488 1115912 1117328 1118248 1118670 1119673 1120088 1122433 1122848 1123270 1124688 1126950 1127033 1127448 1129288 1130715 1131550 1132048 1135315 1135728 1136150 1136648 1139915 1140328 1140750 1141248 1142675 1144928 1145350 1147275 1147688 1148110 1150035 1150448 1152288 1152710 1153715 1155048 1155470 1156475 1158315 1158728 1159235 1160070 1161075 1161488 1161910 1164248 1166088 1166510 1170688 1171608 1172030 1176208 1176630 1179888 1181230 1182648 1185408 1187248 1187668 1190008 1191848 1192268 1193686 1196234 1196446 1198286 1198708 1201046 1201468 1202886 1203806 1205646 1207691 1207907 1208406 1208611 1210246 1210451 1212086 1212291 1212794 1213006 1213209 1213427 1214848 1216688 1216889 1217394 1217608 1219448 1221288 1221489 1222208 1222627 1223834 1224048 1224249 1225886 1226806 1228434 1228646 1228849 1229065 1230486 1233246 1233449 1235086 1235794 1236006 1236425 1238049 1239686 1242234 1242446 1242649 1242863 1245206 1246983 1246988 1247249 1247912 1247915 1247917 1247920 1247966 1249762 1249765 1249767 1249768 1249806 1250223 1251434 1251612 1251613 1251616 1251618 1252541 1252543 1252545 1252566 1252769 1254388 1254390 1254391 1254395 1254396 1254400 1254401 1254403 1254405 1254406 1254408 1254410 1254411 1254413 1254415 1254416 1254418 1254420 1254421 1254423 1256263 1256265 1256266 1256268 1256270 1256271 1256273 1256275 1256276 1256278 1256280 1256281 1256954 1257166 1257369 1257583 1260846 1263606 1263809 1264023 1265234 1265446 1266366 1267776 1268623 1270966 1271169 1272594 1272806 1273223 1275138 1275566 1275769 1276978 1277192 1277823 1279246 1279738 1280369 1281792 1282006 1282423 1283418 1284969 1286178 1286392 1286606 1287023 1288446 1288940 1289569 1289783 1290992 1291206 1293046 1293540 1294171 1294383 1295592 1295806 1297220 1297646 1297851 1298566 1298983 1300191 1300405 1301821 1302245 1302451 1303165 1304791 1305005 1305211 1305423 1306421 1306845 1307551 1307765 1307971 1308183 1309605 1311021 1311445 1312151 1312571 1312783 1315623 1315831 1316005 1316007 1316008 1316010 1316012 1316015 1316016 1316020 1316023 1316025 1316030 1316251 1316915 1316953 1316955 1316956 1316960 1316961 1316963 1316965 1316966 1316968 1316970 1316973 1317383 1318591 1318815 1318816 1318820 1318821 1319011 1320223 1320665 1320666 1320668 1320670 1320671 1320673 1320675 1320676 1320678 1321063 1321351 1321600 1321601 1321603 1321605 1321606 1321771 1323448 1323450 1323451 1323453 1323455 1323456 1324823 1325031 1326371 1326583 1327791 1329425 1330051 1330263 1330551 1332600 1332811 1333105 1333311 1333520 1333943 1335571 1336991 1337200 1337623 1337705 1338331 1339751 1339960 1341385 1341591 1342011 1342223 1342720 1344351 1344771 1344983 1345986 1346400 1347111 1347531 1349371 1349583 1350791 1351000 1351506 1352131 1352343 1353346 1353551 1353760 1355391 1355811 1356023 1356520 1358151 1358571 1359786 1360411 1360623 1361120 1362546 1362751 1363171 1364386 1364800 1365223 1365306 1365511 1365931 1367771 1369400 1369823 1369908 1370111 1370531 1372583 1373588 1374000 1374211 1374711 1376760 1376971 1377182 1378188 1379311 1379520 1379731 1379942 1380948 1383200 1383409 1383622 1383911 1385548 1385960 1386169 1386382 1388308 1388511 1388720 1388929 1389142 1390351 1390560 1391988 1392400 1392609 1393320 1393740 1394748 1394951 1395160 1395369 1395580 1396588 1397000 1397420 1397711 1397920 1398129 1399760 1400180 1401188 1401600 1401809 1402108 1402311 1402520 1402729 1402940 1404360 1405788 1405991 1406200 1406409 1406620 1407120 1407329 1407540 1408546 1408751 1408960 1410800 1411009 1411220 1411306 1411511 1411718 1413146 1413558 1413769 1415189 1415609 1415820 1415906 1416318 1417949 1418158 1418369 1418582 1418666 1419289 1420506 1420709 1420916 1421342 1422346 1422756 1422969 1423889 1424102 1425105 1425309 1425516 1426945 1427149 1427356 1427569 1427782 1428487 1429705 1429909 1430116 1430327 1430542 1431545 1431956 1432167 1432382 1432465 1432667 1432876 1433087 1434927 1435142 1436145 1436347 1436556 1436767 1437065 1437267 1437476 1437687 1437902 1438905 1439316 1439527 1439742 1440745 1440947 1441367 1441582 1441867 1442076 1442287 1442502 1443503 1443505 1443707 1443916 1444127 1444342 1445343 1445547 1445756 1445967 1446182 1446263 1446467 1446887 1447102 1448103 1448307 1448516 1448727 1448774 1448777 1448779 1448942 1449943 1450147 1450356 1450567 1450602 1450607 1450863 1451067 1451487 1451514 1451516 1451702 1452703 1453116 1453327 1453341 1453351 1453543 1454543 1454956 1455167 1455176 1455181 1455383 1455463 1455876 1456084 1456087 1456303 1457303 1457917 1457921 1457927 1458097 1458143 1459141 1459556 1459749 1459751 1459754 1459938 1459940 1459943 1459983 1460061 1460476 1460664 1460687 1460863 1460867 1460868 1460870 1461901 1462527 1462710 1462712 1462713 1462715 1462717 1462718 1462722 1462723 1462725 1462728 1462742 1462743 1464156 1464570 1464573 1464575 1464577 1464578 1464580 1464582 1465287 1466915 1466916 1467127 1468755 1468967 1471727 1473355 1473567 1474275 1474487 1476115 1477955 1478167 1479087 1480715 1480927 1482555 1483475 1483687 1485315 1485527 1487155 1488075 1488287 1489915 1490127 1492887 1494727 1496567 1497487 1499326 1500246 ];
L = superpixels(X,7902);
BW = lazysnapping(X,L,foregroundInd,backgroundInd);

% Create masked image.
maskedImage = X;
maskedImage(~BW) = 0;
end

