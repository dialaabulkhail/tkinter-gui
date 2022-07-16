import paramiko
from paramiko_expect import SSHClientInteraction
from re import findall


## new
import tkinter as tk

root = tk.Tk()



root.mainloop()


#Get the INPUT
Route=input("Route Name:")
RouteI=Route+"I"
RouteO=Route+"O"
SNB=input("PILOT number:")
MGW_Number=input("MGW#:")
EXTP=input("EXTP:")
PBX=input("PBX Name:")

#print (MGW_Number)    
     
 
if MGW_Number=="1": 
 mg="hqmgw01"
 DEST="test"
 MGG="HQMGW1R"

if MGW_Number=="2": 
 mg="hqmgw02"
 DEST="HQMGW02"
 MGG="HQMGW2R"
 

if MGW_Number=="3": 
 mg="AAMGW03"
 DEST="MGW3"
 MGG="AAMGW3R"

if MGW_Number=="4": 
 mg="AAMGW04"
 DEST="MGW4"
 MGG="AAMGW4R"
 

ssh = paramiko.SSHClient()
# make sure that any host is permitted to be accessed even if it doesnt exist in the known host file
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
if MGW_Number=="1": IP="172.16.28.4"
if MGW_Number=="2": IP="172.16.28.4"
if MGW_Number=="3": IP="172.16.44.4"
if MGW_Number=="4": IP="172.16.44.4"
user = 'tariqz'
pasito = 'Zain@1234#4'
PROMPT = '.*>\s*'
ssh.connect(IP, port=22, username=user, password=pasito, look_for_keys=False)
with SSHClientInteraction(ssh, timeout=200, display=False) as interact:
     #Run the first command and capture the cleaned output, if you want
     #the output without cleaning, simply grab current_output instead.



     ## IID
     if MGW_Number=="1": interact.send('mml -cp cp1 EXUAP:DEST=test,IIDTYPE=ALL;')
     if MGW_Number=="2": interact.send('mml -cp cp1 EXUAP:DEST=HQMGW02,IIDTYPE=ALL;')
     if MGW_Number=="3": interact.send('mml -cp cp1 EXUAP:DEST=MGW3,IIDTYPE=ALL;')
     if MGW_Number=="4": interact.send('mml -cp cp1 EXUAP:DEST=MGW4,IIDTYPE=ALL;') 
     interact.expect(PROMPT)
     xiid = interact.current_output


     ## HU
     interact.send('mml -cp cp1 exnsp:hu=all;')
     interact.expect(PROMPT)
     xhu = interact.current_output


     ## RTDMA, DEV 
     interact.send('mml -cp cp1 ntcop:snt=all;')
     interact.expect(PROMPT)
     xntcop = interact.current_output


     ## RC
     interact.send('mml -cp cp1 anrsp:rc=all;')
     interact.expect(PROMPT)
     xrc = interact.current_output


     ## PREFIX
     interact.send('mml -cp cp1 anbsp:b=25;')
     interact.expect(PROMPT)
     xprefix = interact.current_output


     interact.send('exit')
     interact.expect(PROMPT)
     ssh.close()
  


#EXTP:

MSE=EXTP[0]
Slotx=EXTP[1]+EXTP[2]
MSE=int(MSE)-2
MSE=str(MSE)



slot=Slotx
if Slotx=="01": slot="1"
if Slotx=="02": slot="2"
if Slotx=="03": slot="3"
if Slotx=="04": slot="4"
if Slotx=="05": slot="5"
if Slotx=="06": slot="6"
if Slotx=="07": slot="7"
if Slotx=="08": slot="8"
if Slotx=="09": slot="9"

Os='MSE'+MSE+'-'+slot+'-'+EXTP[3]



Vc=EXTP[4]+EXTP[5]

if Vc=="01": Vc="1"
if Vc=="02": Vc="2"
if Vc=="03": Vc="3"
if Vc=="04": Vc="4"
if Vc=="05": Vc="5"
if Vc=="06": Vc="6"
if Vc=="07": Vc="7"
if Vc=="08": Vc="8"
if Vc=="09": Vc="9"


DChannel=Os+'-'+Vc


 
#IID
IID0=list(map(int, findall(r'\w\-\d+\s+(\d+)',xiid)))
IIDNUM = IID0.count(IID0)
IID=IID0[IIDNUM-1]+1


#print(IID)
     
     
MAX_HU_Number = 600

#SNB

## WHERE TO USE?
numbers = sum(c.isdigit() for c in SNB)   #how many numbers is the SNB 
SNBX=list(SNB)
SNBX[numbers-1]=0
SNBX[numbers-2]=0
#print (Num)
SNBX= "".join(str(n) for n in SNBX)
#print (Num)
#print(SNBX)


#Prefix
PRFX0= list(map(int, findall(r'\d+\D+\d\d\d\d(\d\d\d)\s+RC',xprefix)))
#PRFX0=PRFX0[i] <900
#print(PRFX0)
#Unused_Prefix=list(range(800,900))
#print(Unused_Prefix)

Unused_Prefix = list(set(list(range(PRFX0[0],PRFX0[0]+98))) - set(PRFX0))
#print (Unused_Prefix)
if MGW_Number=="3":Unused_Prefix.remove(888)
if MGW_Number=="4":Unused_Prefix.remove(888)

prefix=Unused_Prefix[0]
#print(Unused_Prefix)
#print (prefix)


#RC
RC0 = list(map(int, findall(r'(\d+)\s+NO',xrc)))
RCNUM = RC0.count(RC0)
RC=RC0[RCNUM-1]+1
#print(RC)



#HU
hus = list(map(int, findall(r'(\d+)\s+\d+\s+0',xhu)))
SNBs = list(map(int, findall(r'\d+\s+(\d+)\s+0',xhu)))
unused_hu = list(set(list(range(MAX_HU_Number))) - set(hus))
unused_hu.sort()
#print (SNBs)
#print (hus)
#print (unused_hu)
HU=unused_hu[0]
#print(HU)

#RTDMA
RTDMA0 = list(map(int, findall(r'\w\-(\d+)\s+2',xntcop)))
RTDMANUM = RTDMA0.count(RTDMA0)
RTDMA=RTDMA0[RTDMANUM-1]+1
#print (RTDMA)

#DEV
DEV0 = list(map(int, findall(r'\w\-\d+\&\&\-(\d+)\s+2',xntcop)))
DEVNUM = DEV0.count(DEV0)
DEV1=DEV0[DEVNUM-1]+1
DEV31=DEV1+31
DEV15=DEV1+15
DEV17=DEV1+17
DEV2=DEV1+1
DEV16=DEV1+16

#print (DEV1)




print()
print()
print()
print("#########################")
print("######SPX commands:######")
print("#########################")
print()
print()
print()
print()
print()
print()


# print ("EXROI:R="+str(RouteI)+"&"+str(RouteO)+",DETY=ADJI,FNC=3;")
# if SNB not in SNBs: print ("EXNSI:HU="+str(HU)+",SNB="+str(SNB)+",l=0;")
# print ("NTCOI:SNT=rtdma-"+str(RTDMA)+",sntv=2,mg="+str(mg)+",extp=2-2-"+str(EXTP)+";")
# print ("EXDUI:DEV=LIPRRMG-"+str(DEV1)+"&&-"+str(DEV31)+",SNT=rtdma-"+str(RTDMA),";")
# print ("EXUAI:DEST="+str(DEST)+",DEV=LIPRRMG-"+str(DEV16)+",IID="+str(IID)+";")
# print ("DTDII:DIP="+str(RTDMA)+"DIP,SNT=rtdma-"+str(RTDMA)+";")
# print ("IUPBI:PBX="+str(PBX)+",SNB="+str(SNB)+",REFP=2,PROTVAR=DSS1E;")
# print ("IUPDI:PBX="+str(PBX)+",DEV=LIPRRMG-"+str(DEV2)+"&&-"+str(DEV15)+"&-"+str(DEV17)+"&&-"+str(DEV31)+";")
# print ("IUPVi:PBX="+str(PBX)+",DEV=LIPRRMG-"+str(DEV2)+"&&-"+str(DEV15)+"&-"+str(DEV17)+"&&-"+str(DEV31)+",SNB="+SNB+";")
# print ("IUPHI:PBX="+str(PBX)+",HG=1,DEV=LIPRRMG-"+str(DEV2)+"&&-"+str(DEV15)+"&-"+str(DEV17)+"&&-"+str(DEV31)+";")
# print ("IUPHC:PBX="+str(PBX)+",BS=SPEECH-1&AUDIO-1&TPHY-1&UDI-1&FAX23-1,HT=0,HG=1;")
# print ("IUSCC:SNB="+str(SNB)+",BS=AUDIO-1&TPHY-1&FAX23-1&UDI-1&SPEECH-1;")
# print ("IUSCC:SNB="+str(SNB)+",PROP=CDPNL-4&CDPNMOD-4&FO-6&TGR-17&DDISRQ-0&REFPNT-2;")
# print ("IUSCC:SNB="+str(SNB)+",SS=COLP-1&CLIP-1&UUS1-1;")
# print ("NTBLE:SNT=rtdma-"+str(RTDMA)+";")
# print ("DTBLE:DIP="+str(RTDMA)+"DIP;")
# print ("BLODI:DEV=LIPRRMG-"+str(DEV1)+"&&-"+str(DEV15)+"&-"+str(DEV17)+"&&-"+str(DEV31)+";")
# print ("EXDRI:R="+str(RouteO)+"&"+str(RouteI)+",DEV=LIPRRMG-"+str(DEV2)+"&&-"+str(DEV15)+"&-"+str(DEV17)+"&&-"+str(DEV31)+";")
# print ("IUMGI:DEV=LIPRRMG-"+str(DEV1),",MGG="+str(MGG)+";")
# print ("BLODE:DEV=LIPRRMG-"+str(DEV1)+"&&-"+str(DEV15)+"&-"+str(DEV17)+"&&-"+str(DEV31)+";")
# print ("ANRPI:RC="+str(RC)+",cch=no;")
# print ("ANRSI:p01=1,sp=mm1,SNB="+str(SNB)+";")
# print ("ANRPE;")
# print ("ANRAI:RC="+str(RC)+";")
# print ("IUSCC:SNB="+str(SNB)+",PROP=OBA-1;")
# print ("ANBLI;")
# print ("ANBZI;")
# print ("ANBCI;")
# print ("ANBSI:B=25-#1113"+str(prefix)+",RC="+str(RC)+",L=8-15,M=6,CC=1;")
# print ("ANBSI:B=85-#1113"+str(prefix)+",RC="+str(RC)+",L=8-15,M=6,CC=1;")
# print ("ANBAI;")

print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()
print()







print("#########################")
print("######MGW commands:######")
print("#########################")
# print('ECHO"=====>> Creating Ds0Bundle #02#"')


#  ECHO"=====>> Creating Ds0Bundle #02#"


# print("CREATE")

#  CREATE
# print("(")
#  (

# print('parent  "ManagedElement=1,Equipment=1,Subrack=MSE'+str(MSE)+',Slot='+str(slot)+',PlugInUnit=1,ExchangeTerminal=1,Os155SpiTtp='+str(Os)+',Vc4Ttp=1,Vc12Ttp='+str(Vc)+',E1Ttp=1"')
#  parent  "ManagedElement=1,Equipment=1,Subrack=MSE1,Slot=17,PlugInUnit=1,ExchangeTerminal=1,Os155SpiTtp=MSE1-17-3,Vc4Ttp=1,Vc12Ttp=45,E1Ttp=1"

# print('identity  "'+str(PBX)+'_Ds16"')
#  identity  "PRI_IDCO_Ds16"

# print("moType  Ds0Bundle")
#  moType  Ds0Bundle

# print("exception  none")
#  exception  none

# print("nrOfAttributes  3")
#  nrOfAttributes  3

# print('userLabel String  "'+str(PBX)+'_Ds16"')
#    userLabel String  "PRI_IDCO_Ds16"

# print('listOfTimeSlots Array Integer  1                16   ')
#    listOfTimeSlots Array Integer  1                16     

# print ('tdmMode Boolean  "TRUE"')          
#    tdmMode Boolean  "TRUE"

# print(')')
#  )

# print('ECHO"=====>> Creating Ds0Bundle #02#"')
#  ECHO"=====>> Creating Ds0Bundle #02#"

# print('CREATE')
#  CREATE

# print('(')
#  (

# print('parent  "ManagedElement=1,Equipment=1,Subrack=MSE'+str(MSE)+',Slot='+str(slot)+',PlugInUnit=1,ExchangeTerminal=1,Os155SpiTtp='+str(Os)+',Vc4Ttp=1,Vc12Ttp='+str(Vc)+',E1Ttp=1"')
#  parent  "ManagedElement=1,Equipment=1,Subrack=MSE1,Slot=17,PlugInUnit=1,ExchangeTerminal=1,Os155SpiTtp=MSE1-17-3,Vc4Ttp=1,Vc12Ttp=45,E1Ttp=1"

# print('identity  "'+str(PBX)+'"')
#  identity  "PRI_IDCO"

# print("moType  Ds0Bundle")
#  moType  Ds0Bundle

# print("exception  none")
#  exception  none

# print("nrOfAttributes  3")
#  nrOfAttributes  3

# print('userLabel String  "'+str(PBX)+'"')
#    userLabel String  "PRI_IDCO"

# print('listOfTimeSlots Array Integer  30 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15  17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 ')
#    listOfTimeSlots Array Integer  30 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15  17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 

# print('tdmMode Boolean  "TRUE"')
#    tdmMode Boolean  "TRUE"

# print(')')
#  )

# print('//==================')
#  //==================

# print('ECHO"=====>> Creating TdmTermGrp #02#"')
#  ECHO"=====>> Creating TdmTermGrp #02#"

# print('CREATE')
#  CREATE

# print('(')
#  (

# print('parent  "ManagedElement=1,MgwApplication=1"')
#  parent  "ManagedElement=1,MgwApplication=1"

# print('identity  "'+str(PBX)+'"')
#  identity  "PRI_IDCO"

# print('moType  TdmTermGrp')
#  moType  TdmTermGrp

# print('exception  none')
#  exception  none

# print('nrOfAttributes  4')
#  nrOfAttributes  4

# print('userLabel String  "'+str(PBX)+'"')
#    userLabel String  "PRI_IDCO"


# print ('ds0BundleMoRef Reference')
#    ds0BundleMoRef Reference 

# print('"ManagedElement=1,Equipment=1,Subrack=MSE'+str(MSE)+',Slot='+str(slot)+',PlugInUnit=1,ExchangeTerminal=1,Os155SpiTtp='+str(Os)+',Vc4Ttp=1,Vc12Ttp='+Vc+',E1Ttp=1,Ds0Bundle='+str(PBX)+'"')
# "ManagedElement=1,Equipment=1,Subrack=MSE1,Slot=17,PlugInUnit=1,ExchangeTerminal=1,Os155SpiTtp=MSE1-17-3,Vc4Ttp=1,Vc12Ttp=45,E1Ttp=1,Ds0Bundle=PRI_IDCO"

# print('pcmSystemNr Integer  "'+str(EXTP)+'"')
#    pcmSystemNr Integer  "317345"

# print('partialFill Integer  "40"')
#    partialFill Integer  "40"

# print(')')
#  )


# print('ECHO "===>> Creating DChannelTp '+str(DChannel)+'_D"')
#ECHO "===>> Creating DChannelTp MSE1-17-3-45_D"


# print('CREATE')
#  CREATE

# print('(')
#  (

# print('parent "ManagedElement=1,AccessSignalling=1"')
#   parent "ManagedElement=1,AccessSignalling=1"

# print('identity "'+str(PBX)+'_D"')
#   identity "PRI_IDCO_D"

# print('moType DChannelTp')
#   moType DChannelTp

# print('exception none')
#   exception none

# print('nrOfAttributes 5')
#   nrOfAttributes 5

# print('userLabel String "'+str(PBX)+'_D"')
#     userLabel String "PRI_IDCO_D"

# print('ds0BundleMoRef Ref "ManagedElement=1,Equipment=1,Subrack=MSE'+str(MSE)+',Slot='+str(slot)+',PlugInUnit=1,ExchangeTerminal=1,Os155SpiTtp='+str(Os)+',Vc4Ttp=1,Vc12Ttp='+Vc+',E1Ttp=1,Ds0Bundle='+str(PBX)+'_Ds16"')
#     ds0BundleMoRef Ref "ManagedElement=1,Equipment=1,Subrack=MSE1,Slot=17,PlugInUnit=1,ExchangeTerminal=1,Os155SpiTtp=MSE1-17-3,Vc4Ttp=1,Vc12Ttp=45,E1Ttp=1,Ds0Bundle=PRI_IDCO_Ds16"

# print('interfaceIdentifier Integer '+str(IID))
#     interfaceIdentifier Integer 20  

# print('lapdSapProfileMoRef Ref "ManagedElement=1,AccessSignalling=1,LapdSapProfile=1"')
#     lapdSapProfileMoRef Ref "ManagedElement=1,AccessSignalling=1,LapdSapProfile=1"

# print('lapdMoRef Ref "ManagedElement=1,AccessSignalling=1,Lapd=CTRL-24"')
#     lapdMoRef Ref "ManagedElement=1,AccessSignalling=1,Lapd=CTRL-24"

# print(')')
#)





print()
print()
print()
print()
print()
print()
print("#########################")
print("######EDA commands:######")
print("#########################")
print()
print()
print()
print()
print()
print()

# print('HGSDC:MSISDN=962'+str(SNB)+',SUD=CFU-1;')
# print('HGSDC:MSISDN=962'+str(SNB)+',SUD=CSP-19;')
print('HGSSI:MSISDN=962'+str(SNB)+',SS=CFS,BSG=TS10,FNUM="#13'+str(prefix)+str(SNB)+'",OFA=512;')




#EXROI:R=IDCOPRI&IDCOPRO,DETY=ADJI,FNC=3;
#EXNSI:HU=410,SNB=26911100,l=0; 
#NTCOI:SNT=rtdma-245,sntv=2,mg=hqmgw01,extp=2-2-317345;
#EXDUI:DEV=LIPRRMG-7840&&-7871,SNT=rtdma-245;
#EXUAI:DEST=test,DEV=LIPRRMG-7856,IID=20;
#DTDII:DIP=245DIP,SNT=rtdma-245;
#IUPBI:PBX=PRI_IDCO,SNB=26911110,REFP=2,PROTVAR=DSS1E;
#IUPDI:PBX=PRI_IDCO,DEV=LIPRRMG-7841&&-7855&-7857&&-7871;
#IUPVi:PBX=PRI_IDCO,DEV=LIPRRMG-7841&&-7855&-7857&&-7871,SNB=26911110;
#IUPHI:PBX=PRI_IDCO,HG=1,DEV=LIPRRMG-7841&&-7855&-7857&&-7871;
#IUPHC:PBX=PRI_IDCO,BS=SPEECH-1&AUDIO-1&TPHY-1&UDI-1&FAX23-1,HT=0,HG=1;
#IUSCC:SNB=26911110,BS=AUDIO-1&TPHY-1&FAX23-1&UDI-1&SPEECH-1;
#IUSCC:SNB=26911110,PROP=CDPNL-4&CDPNMOD-4&FO-6&TGR-17&DDISRQ-0&REFPNT-2;
#IUSCC:SNB=26911110,SS=COLP-1&CLIP-1&UUS1-1;
#NTBLE:SNT=rtdma-245;
#DTBLE:DIP=245DIP;
#BLODI:DEV=LIPRRMG-7840&&-7855&-7857&&-7871;
#EXDRI:R=IDCOPRO&IDCOPRI,DEV=LIPRRMG-7841&&-7855&-7857&&-7871;
#IUMGI:DEV=LIPRRMG-7840,MGG=HQMGW1R;
#BLODE:DEV=LIPRRMG-7840&&-7855&-7857&&-7871;
#ANRPI:RC=304,cch=no;
#ANRSI:p01=1,sp=mm1,SNB=26911110;
#ANRPE;
#ANRAI:RC=304; 
#IUSCC:SNB=26911110,PROP=OBA-1;
#ANBLI;
#ANBZI;
#ANBCI;

# to run application
