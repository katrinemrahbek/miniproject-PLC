PROGRAM PLC_PRG
VAR
	TCP				:	DC_ECP.TcpClientByteStream;
	timer			:	TON;
	RFID			:	dc_ecp.Dtm425;
	rfidData		:	dc_ecp.st_CPF_RfidData;
	carrierID: UINT;
	state: INT := 0;
	palletID: UINT;
	dataOut: STRING;
	stationID: UINT := 5;
	dataIn: UINT;
	timeinSec: TIME;
END_VAR

timer();
RFID();
TCP();

CASE state OF
	0:
	rfid.ClearError();
	TCP.Reset();
	
	state :=1;
	
	1: // wait for rfid and tcp to be ready an then connect
	IF rfid.xReady AND TCP.xReady THEN
		rfid.Connect(usiNodeId := 32, usiNetworkId := 0, usiChannel := 1);
		TCP.Connect(sIP:= '172.20.66.112', uiPort:=9999); 
		state := 2;
	END_IF
	
	2: // when connected start conveyer belt
		IF rfid.xReady AND TCP.xConnected THEN
			GVL.xQA1_LEFT :=FALSE;
			GVL.xQA1_RIGHT :=TRUE;
			GVL.xQA1_SLOW :=FALSE;
			state:= 10;
		END_IF
	
	10: // when pallet runs over carrierbit 2 change conveyer belt to slow
	IF GVL.xBG24 = TRUE THEN
		GVL.xQA1_SLOW := TRUE;
		state :=11;
	END_IF

	11: // when the conveyer is at the stopper the belt is stopped
	IF GVL.xBG21=TRUE THEN
		GVL.xQA1_RIGHT := FALSE;
		state := 12;
	END_IF
	
	12:// the rfidtag is read
		rfid.ReadTag(uiStartAddress:=0,uiDataLength:=SIZEOF(rfidData), pData:=ADR(rfidData));
		state := 13;
		
	13:// the station id and carrier id is put into a string and send. The processing time is recieved.
	IF rfid.xReady THEN
			
		palletID := dc_ecp.SwapWORD(rfidData.uiCarrierID);
		dataOut:=':<station id = "';
		dataOut:=CONCAT(dataOut,UINT_TO_STRING(stationID));
		dataOut:=CONCAT(dataOUT, '"><carrierID>');
		dataOut:=CONCAT(dataOUT,UINT_TO_STRING(carrierID));
		dataOut:=CONCAT(dataOut, '</carrierID></station>;');
			
			
		TCP.SendAndReceive(pToSend:=ADR(dataOut), uiSizeToSend:= SIZEOF(dataOut),pToReceive:=ADR(dataIn),uiSizeToReceive:=SIZEOF(dataIn));
		state:=14;
	END_IF	
			
		
	14:// The processing time is put into a timer
	IF TCP.xReady THEN
		state:=15;
		timeinSec:=(INT_TO_TIME(STRING_TO_INT(dataIn)));
		TCP.Disconnect();
		timer(IN:=FALSE);
		timer();
		timer(IN:=TRUE, PT:=timeinSec);
	END_IF
	
		
	15: // when the timer is done the stopper is put down and the belt restarted
		IF timer.Q THEN
			GVL.xQA1_RIGHT := TRUE;
			GVL.xMB20 := TRUE;
			state:=16;
		END_IF
		
		
	16: // then when carrier has left set it to fast speed again
	IF GVL.xBG21=FALSE THEN
		GVL.xQA1_SLOW := FALSE;
		state:= 2;
	END_IF
	

		
END_CASE
	