import tkinter as tk
import paramiko
from paramiko_expect import SSHClientInteraction
from re import findall


def fun(Route, SNB, MGW_Number, EXTP, PBX):
    RouteI = Route+"I"
    RouteO = Route+"O"

    if MGW_Number == "1":
        mg = "hqmgw01"
        DEST = "test"
        MGG = "HQMGW1R"

    if MGW_Number == "2":
        mg = "hqmgw02"
        DEST = "HQMGW02"
        MGG = "HQMGW2R"

    if MGW_Number == "3":
        mg = "AAMGW03"
        DEST = "MGW3"
        MGG = "AAMGW3R"

    if MGW_Number == "4":
        mg = "AAMGW04"
        DEST = "MGW4"
        MGG = "AAMGW4R"

       # MUST TEST SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if MGW_Number == "1":
        IP = "172.16.28.4"
    if MGW_Number == "2":
        IP = "172.16.28.4"
    if MGW_Number == "3":
        IP = "172.16.44.4"
    if MGW_Number == "4":
        IP = "172.16.44.4"

    # MAKE A NEW ENTRY FOR USER INFO
    # user = 'tariqz'
    # pasito = 'Zain@1234#4'

    PROMPT = '.*>\s*'
    # ssh.connect(IP, port=22, username=user, password=pasito, look_for_keys=False)

    with SSHClientInteraction(ssh, timeout=200, display=False) as interact:
        #    #Run the first command and capture the cleaned output, if you want
        #    #the output without cleaning, simply grab current_output instead.

        ## IID - extract
        if MGW_Number == "1":
            interact.send('mml -cp cp1 EXUAP:DEST=test,IIDTYPE=ALL;')
        if MGW_Number == "2":
            interact.send('mml -cp cp1 EXUAP:DEST=HQMGW02,IIDTYPE=ALL;')
        if MGW_Number == "3":
            interact.send('mml -cp cp1 EXUAP:DEST=MGW3,IIDTYPE=ALL;')
        if MGW_Number == "4":
            interact.send('mml -cp cp1 EXUAP:DEST=MGW4,IIDTYPE=ALL;')
        interact.expect(PROMPT)
        xiid = interact.current_output

        ## HU - extract
        interact.send('mml -cp cp1 exnsp:hu=all;')
        interact.expect(PROMPT)
        xhu = interact.current_output

        ## RTDMA, DEV - extract
        interact.send('mml -cp cp1 ntcop:snt=all;')
        interact.expect(PROMPT)
        xntcop = interact.current_output

    #   ## RC
        interact.send('mml -cp cp1 anrsp:rc=all;')
        interact.expect(PROMPT)
        xrc = interact.current_output

        # PREFIX
        interact.send('mml -cp cp1 anbsp:b=25;')
        interact.expect(PROMPT)
        xprefix = interact.current_output

        interact.send('exit')
        interact.expect(PROMPT)
        ssh.close()

    ## HU, SNB - clean
    MAX_HU_Number = 600
    hus = list(map(int, findall(r'(\d+)\s+\d+\s+0', xhu)))
    SNBs = list(map(int, findall(r'\d+\s+(\d+)\s+0', xhu)))
    unused_hu = list(set(list(range(MAX_HU_Number))) - set(hus))
    unused_hu.sort()
    HU = unused_hu[0]

    ## RTDMAO - clean
    RTDMA0 = list(map(int, findall(r'\w\-(\d+)\s+2', xntcop)))
    RTDMANUM = RTDMA0.count(RTDMA0)
    RTDMA = RTDMA0[RTDMANUM-1]+1

    ## DEV - clean
    DEV0 = list(map(int, findall(r'\w\-\d+\&\&\-(\d+)\s+2', xntcop)))
    DEVNUM = DEV0.count(DEV0)
    DEV1 = DEV0[DEVNUM-1]+1
    DEV31 = DEV1+31
    DEV15 = DEV1+15
    DEV17 = DEV1+17
    DEV2 = DEV1+1
    DEV16 = DEV1+16

    ## IID - clean
    IID0 = list(map(int, findall(r'\w\-\d+\s+(\d+)', xiid)))
    IIDNUM = IID0.count(IID0)
    IID = IID0[IIDNUM-1]+1

    ## RC = clean
    RC0 = list(map(int, findall(r'(\d+)\s+NO', xrc)))
    RCNUM = RC0.count(RC0)
    RC = RC0[RCNUM-1]+1

    ## PREFIX - clean
    PRFX0 = list(map(int, findall(r'\d+\D+\d\d\d\d(\d\d\d)\s+RC', xprefix)))
    Unused_Prefix = list(set(list(range(PRFX0[0], PRFX0[0]+98))) - set(PRFX0))
    if MGW_Number == "3":
        Unused_Prefix.remove(888)
    if MGW_Number == "4":
        Unused_Prefix.remove(888)
    prefix = Unused_Prefix[0]

    # MGW COMMANDS DATA PREPARING
    MSE = EXTP[0]
    Slotx = EXTP[1]+EXTP[2]
    MSE = int(MSE)-2
    MSE = str(MSE)

    slot = Slotx
    if Slotx == "01":
        slot = "1"
    if Slotx == "02":
        slot = "2"
    if Slotx == "03":
        slot = "3"
    if Slotx == "04":
        slot = "4"
    if Slotx == "05":
        slot = "5"
    if Slotx == "06":
        slot = "6"
    if Slotx == "07":
        slot = "7"
    if Slotx == "08":
        slot = "8"
    if Slotx == "09":
        slot = "9"

    Os = 'MSE'+MSE+'-'+slot+'-'+EXTP[3]

    Vc = EXTP[4]+EXTP[5]

    if Vc == "01":
        Vc = "1"
    if Vc == "02":
        Vc = "2"
    if Vc == "03":
        Vc = "3"
    if Vc == "04":
        Vc = "4"
    if Vc == "05":
        Vc = "5"
    if Vc == "06":
        Vc = "6"
    if Vc == "07":
        Vc = "7"
    if Vc == "08":
        Vc = "8"
    if Vc == "09":
        Vc = "9"

    DChannel = Os+'-'+Vc

    # THE SCRIPT OF SPX COMMANDS
    routeLine = "EXROI:R="+str(RouteI)+"&"+str(RouteO)+",DETY=ADJI,FNC=3;"
    if SNB not in SNBs:
        huLine = "EXNSI:HU="+str(HU)+",SNB="+str(SNB)+",l=0;"
    rtdma = "NTCOI:SNT=rtdma-" + str(RTDMA)+",sntv=2,mg="+str(mg)+",extp=2-2-"+str(EXTP)+";"
    dev = "EXDUI:DEV=LIPRRMG-"+str(DEV1)+"&&-" + str(DEV31)+",SNT=rtdma-"+str(RTDMA), ";"
    iid = "EXUAI:DEST="+str(DEST)+",DEV=LIPRRMG-" + str(DEV16)+",IID="+str(IID)+";"
    rtdma2 = "DTDII:DIP="+str(RTDMA)+"DIP,SNT=rtdma-"+str(RTDMA)+";"
    pbx_snb = "IUPBI:PBX="+str(PBX)+",SNB="+str(SNB)+",REFP=2,PROTVAR=DSS1E;"
    devs = "IUPDI:PBX="+str(PBX)+",DEV=LIPRRMG-"+str(DEV2) + "&&-"+str(DEV15)+"&-"+str(DEV17)+"&&-"+str(DEV31)+";"
    dev_snb_pbx = "IUPVi:PBX="+str(PBX)+",DEV=LIPRRMG-"+str(DEV2)+"&&-"+str(DEV15)+"&-"+str(DEV17)+"&&-"+str(DEV31)+",SNB="+SNB+";"
    pbx_dev = "IUPHI:PBX="+str(PBX)+",HG=1,DEV=LIPRRMG-"+str(DEV2) + "&&-"+str(DEV15)+"&-"+str(DEV17)+"&&-"+str(DEV31)+";"
    pbx = "IUPHC:PBX=" + str(PBX)+",BS=SPEECH-1&AUDIO-1&TPHY-1&UDI-1&FAX23-1,HT=0,HG=1;"
    snb = "IUSCC:SNB="+str(SNB)+",BS=AUDIO-1&TPHY-1&FAX23-1&UDI-1&SPEECH-1;"
    snb2 = "IUSCC:SNB=" + str(SNB)+",PROP=CDPNL-4&CDPNMOD-4&FO-6&TGR-17&DDISRQ-0&REFPNT-2;"
    snb3 = "IUSCC:SNB="+str(SNB)+",SS=COLP-1&CLIP-1&UUS1-1;"
    rtdma3 = "NTBLE:SNT=rtdma-"+str(RTDMA)+";"
    rtdma4 = "DTBLE:DIP="+str(RTDMA)+"DIP;"
    devs2 = "BLODI:DEV=LIPRRMG-" + str(DEV1)+"&&-"+str(DEV15)+"&-"+str(DEV17)+"&&-"+str(DEV31)+";"
    devs_router = "EXDRI:R="+str(RouteO)+"&"+str(RouteI)+",DEV=LIPRRMG-"+str(DEV2)+"&&-"+str(DEV15)+"&-"+str(DEV17)+"&&-"+str(DEV31)+";"
    mgg = "IUMGI:DEV=LIPRRMG-"+str(DEV1), ",MGG="+str(MGG)+";"
    devs3 = "BLODE:DEV=LIPRRMG-" + str(DEV1)+"&&-"+str(DEV15)+"&-"+str(DEV17)+"&&-"+str(DEV31)+";"
    rc = "ANRPI:RC="+str(RC)+",cch=no;"
    snb4 = "ANRSI:p01=1,sp=mm1,SNB="+str(SNB)+";"
    string = "ANRPE;"
    rc2 = "ANRAI:RC="+str(RC)+";"
    snb5 = "IUSCC:SNB="+str(SNB)+",PROP=OBA-1;"
    string2 = "ANBLI;"
    string3 = "ANBZI;"
    string4 = "ANBCI;"
    prefix1 = "ANBSI:B=25-#1113"+str(prefix)+",RC="+str(RC)+",L=8-15,M=6,CC=1;"
    prefix2 = "ANBSI:B=85-#1113"+str(prefix)+",RC="+str(RC)+",L=8-15,M=6,CC=1;"
    string5 = "ANBAI;"

    # THE SCRIPT OF MGW COMMANDS
    mse_slot = 'parent  "ManagedElement=1,Equipment=1,Subrack=MSE'+str(MSE)+',Slot='+str(slot)+',PlugInUnit=1,ExchangeTerminal=1,Os155SpiTtp='+str(Os)+',Vc4Ttp=1,Vc12Ttp='+str(Vc)+',E1Ttp=1"'
    pbx_mgw = 'identity  "'+str(PBX)+'_Ds16"'
    pbx_mgw2 = 'userLabel String  "'+str(PBX)+'_Ds16"'
    mse_slot_vs = 'parent  "ManagedElement=1,Equipment=1,Subrack=MSE'+str(MSE)+',Slot='+str(slot)+',PlugInUnit=1,ExchangeTerminal=1,Os155SpiTtp='+str(Os)+',Vc4Ttp=1,Vc12Ttp='+str(Vc)+',E1Ttp=1"'
    pbx_mgw3 = 'identity  "'+str(PBX)+'"'
    pbx_mgw4 = 'userLabel String  "'+str(PBX)+'"'
    msE_slot_vs2 = '"ManagedElement=1,Equipment=1,Subrack=MSE'+str(MSE)+',Slot='+str(slot)+',PlugInUnit=1,ExchangeTerminal=1,Os155SpiTtp='+str(Os)+',Vc4Ttp=1,Vc12Ttp='+Vc+',E1Ttp=1,Ds0Bundle='+str(PBX)+'"'
    pbX_mgw_5 = 'pcmSystemNr Integer  "'+str(EXTP)+'"'
    dchannel = 'ECHO "===>> Creating DChannelTp '+str(DChannel)+'_D"'
    pbx_user = 'userLabel String "'+str(PBX)+'_D"'
    mse_slot_vs3 = 'ds0BundleMoRef Ref "ManagedElement=1,Equipment=1,Subrack=MSE'+str(MSE)+',Slot='+str(slot)+',PlugInUnit=1,ExchangeTerminal=1,Os155SpiTtp='+str(Os)+',Vc4Ttp=1,Vc12Ttp='+Vc+',E1Ttp=1,Ds0Bundle='+str(PBX)+'_Ds16"'
    mgw_iid = 'interfaceIdentifier Integer '+str(IID)

    # THE SCRIPT OF EDA COMMANDS
    eda_snb = 'HGSDC:MSISDN=962'+str(SNB)+',SUD=CFU-1;'
    eda_snb2 = 'HGSDC:MSISDN=962'+str(SNB)+',SUD=CSP-19;'
    eda_snb3 = 'HGSSI:MSISDN=962' + str(SNB)+',SS=CFS,BSG=TS10,FNUM="#13'+str(prefix)+str(SNB)+'",OFA=512;'

        

    # THE OUTPUT SCRIPT OF SPX COMMANDS  + MGW COMMANDS
    output = routeLine + "\n" + huLine + "\n" + rtdma + "\n" + dev + "\n" + iid + "\n" + rtdma2 + "\n" + pbx_snb + "\n" + devs + "\n" + dev_snb_pbx + "\n" + pbx_dev + "\n" + pbx + "\n" + snb + "\n" + snb2 + "\n" + snb3 + "\n" + rtdma3 + "\n" + rtdma4 + "\n" + devs2 + "\n" + devs_router + "\n" + mgg + "\n" + devs3 + "\n" + rc + "\n" + snb4 + "\n" + string + "\n" + rc2 + "\n" + snb5 + "\n" + string2 + "\n" + string3 + "\n" + string4 + "\n" + prefix1 + "\n" + prefix2 + "\n" + string5 + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + 'ECHO"=====>> Creating Ds0Bundle #02#"' + "\n" + "CREATE" + "(" + "\n" + mse_slot + "\n" + pbx_mgw + "\n" + "moType  Ds0Bundle" + "\n" + "exception  none" + "\n" + "nrOfAttributes  3" + "\n" + pbx_mgw2 + "\n" + 'listOfTimeSlots Array Integer  1                16   ' + "\n" + 'tdmMode Boolean  "TRUE"' + "\n" + ")" + "\n" + 'ECHO"=====>> Creating Ds0Bundle #02#"' + "\n" + 'CREATE' + "\n" + "(" + "\n" + mse_slot_vs + "\n" + pbx_mgw3 + "\n" + "moType  Ds0Bundle" + "\n" + "exception  none" + "\n" + "nrOfAttributes  3" + "\n" + pbx_mgw4 + "\n" + 'listOfTimeSlots Array Integer  30 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15  17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 ' + "\n" + 'tdmMode Boolean  "TRUE"' + "\n" + ")" + "\n" + '//==================' + "\n" + 'ECHO"=====>> Creating TdmTermGrp #02#"' + "\n" + 'CREATE' + "\n" + "(" + "\n" + 'parent  "ManagedElement=1,MgwApplication=1"' + "\n" + pbx_mgw3 + "\n" + 'moType  TdmTermGrp' + "\n" + 'exception  none' + "\n" + 'nrOfAttributes  4' + "\n" + pbx_mgw4 + "\n" + 'ds0BundleMoRef Reference' + "\n" + msE_slot_vs2 + "\n" + pbX_mgw_5 + "\n" + 'partialFill Integer  "40"' + "\n" + ")" + "\n" + dchannel + "\n" + 'CREATE' + "\n" + "(" + "\n" + 'parent "ManagedElement=1,AccessSignalling=1"' + "\n" + pbx_mgw3 + "\n" + 'moType DChannelTp' + "\n" + 'exception none' + "\n" + 'nrOfAttributes 5' + "\n" + pbx_user + "\n" + mse_slot_vs3 + "\n" + mgw_iid + "\n" + 'lapdSapProfileMoRef Ref "ManagedElement=1,AccessSignalling=1,LapdSapProfile=1"' + "\n" + 'lapdMoRef Ref "ManagedElement=1,AccessSignalling=1,Lapd=CTRL-24"' + "\n" + ")" + "\n" + "\n" + "\n" + "\n" + "\n" + "\n" + eda_snb + "\n" + eda_snb2 + "\n" + eda_snb3 + "\n"

    script_text.insert("1.0", output)
    print(output)


# login static function
# def formdata(username, password):
#   if username == "admin" and password == "1234":
#     print(True)


root = tk.Tk()

# ## login data
# username_label = tk.Label(root, text="Username:")
# username_label.pack( )
# username = tk.Entry(root, bd =5, exportselection=0)
# username.pack()

# password_label = tk.Label(root, text="Password:")
# password_label.pack( )
# password = tk.Entry(root, bd =5, exportselection=0)
# password.pack()

# button = tk.Button (root, text ="Submit", command=lambda: formdata(username.get(), password.get()))
# button.pack()


L1 = tk.Label(root, text="Route Name:")
L1.pack()
Route = tk.Entry(root, bd=5, exportselection=0)
Route.pack()

L2 = tk.Label(root, text="PILOT number:")
L2.pack()
SNB = tk.Entry(root, bd=5, exportselection=0)
SNB.pack()

L3 = tk.Label(root, text="MGW#:")
L3.pack()
MGW_Number = tk.Entry(root, bd=5, exportselection=0)
MGW_Number.pack()

L4 = tk.Label(root, text="EXTP:")
L4.pack()
EXTP = tk.Entry(root, bd=5, exportselection=0)
EXTP.pack()

L5 = tk.Label(root, text="PBX Name:")
L5.pack()
PBX = tk.Entry(root, bd=5, exportselection=0)
PBX.pack()

button = tk.Button(root, text="Submit", command=lambda: fun(
    Route.get(), SNB.get(), MGW_Number.get(), EXTP.get(), PBX.get()))
button.pack()


# review if can be label with copy text
script_text = tk.Text(root)
script_text.pack()

root.mainloop()
