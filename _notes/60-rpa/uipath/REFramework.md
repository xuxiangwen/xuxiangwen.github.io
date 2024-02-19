# Main

- Arguments

  ![image-20230523155858513](images/image-20230523155858513.png)

- Variables

  ![image-20230523155937407](images/image-20230523155937407.png)

~~~mermaid
flowchart TB
start((start)) --> Initialization
Initialization -->|Successful|GetTransactionData[Get Transaction Data]
Initialization -->|"System Exception<br> (failed initialization)"|EndProcess[End Process]
GetTransactionData --> |No Data|EndProcess
GetTransactionData --> |New Transaction|ProcessTransaction[Process Transaction]
ProcessTransaction --> |System Exception|Initialization
ProcessTransaction --> |Success or Business Exception|GetTransactionData

~~~

Here are transitions.

- Initialization

  - Successful: SystemException is Nothing

  - System Exception (failed initialization): SystemException isNot Nothing

- Get Transaction Data

  - No Data: TransactionItem IsNot Nothing

  - New Transaction: TransactionItem IsNot Nothing

- Process Transaction
  - Success: SystemException Is Nothing And BusinessException is Nothing
  - Business Exception: BusinessException IsNot Nothing
  - System Exception: SystemException IsNot Nothing

## Initialization

- If there is any exception in state, assign it to variable SystemException.

- If maxConsecutiveSystemExceptions exceeded

  ~~~vb
  Cint(Config("MaxConsecutiveSystemExceptions"))>0 AndAlso ConsecutiveSystemExceptions>=Cint(Config("MaxConsecutiveSystemExceptions"))
  ~~~

  

~~~mermaid
flowchart LR
ConfigIsNothing{Config <br>is Nothing} -->|True|InitAllSettings[Invoke<br>InitAllSettings]
InitAllSettings --> SetOrchestratorQueueName[Assign<br>OrchestratorQueueName,<br>OrchestratorQueueFolder]
SetOrchestratorQueueName --> KillAllProcesses[Invoke<br>KillAllProcesses]
KillAllProcesses --> AddLogFields["Add Log Fields<br>(BusinessProcessName)"]
AddLogFields --> maxConsecutive{If <br> maxConsecutive<br>SystemExceptions <br> exceeded}
ConfigIsNothing -->|False|maxConsecutive 
maxConsecutive -->|True|Exception[throw Exception]
maxConsecutive -->|False|InitiAllApplications[Invoke<br>InitiAllApplications]
~~~

### InitAllSettings

- Arguments

![image-20230523164612637](images/image-20230523164612637.png)

- Variables: empty

### InitiAllApplications

- Arguments

  ![image-20230523164908259](images/image-20230523164908259.png)

- Variables: empty

## Get Transaction Data

~~~mermaid
flowchart LR
CheckStopSignal{Check Stop Signal} -->|True|AssignTransactionItem[Assign Nothing to <br>variable TransactionItem]
CheckStopSignal -->|False|GetTransactionData[Invoke GetTransactionData]
subgraph Retry["Try"]
GetTransactionData
end

GetTransactionData --> CatchException{Catch Exception}
CatchException -->|True|AssignTransactionItem
CatchException -->|False|end1((end))


~~~

### GetTransactionData

- Arguments


![image-20230523163032863](images/image-20230523163032863.png)

- Variables: empty

  

~~~mermaid
flowchart LR
subgraph Retry["Retry - RetryNumberGetTransactionItem "]
Gettransactionitem[Get transaction item] 
end
Gettransactionitem --> out_TransactionItem{out_TransactionItem <br>isNot Nothing} 
out_TransactionItem -->|True|Assign1[out_TransactionID=now.ToString<br>out_TransactionField1=string.Empty<br>out_TransactionField2=string.Empty]
~~~

## Process Transaction

~~~mermaid
flowchart LR
subgraph Try["Try"]
direction TB
Assign1[Assign Nothing to <br>BusinessException] --> Process[Invoke Process]
Process 
end
Process --> CatchBusiessRuleException{Catch <br>BusiessRuleException}
CatchBusiessRuleException -->|"True<br>BusinessRuleException"|AssignBusiessRuleException[Assign<br> BusiessException]
AssignBusiessRuleException --> SetTransactionStatus[Invoke<br>SetTransactionStatus]
CatchBusiessRuleException -->|False|CatchException{Catch Exception}
CatchException -->|"True <br>Exception"|AssignException[Assign<br>SystemException]
AssignException --> SetTransactionStatus
CatchException -->|"False <br>Success"|SetTransactionStatus

~~~

### Process

- Arguments

  ![image-20230523163527216](images/image-20230523163527216.png)

- Variables:  empty

### SetTransactionStatus

- Arguments： call it 3 times

  - Success

    ![image-20230523163155645](images/image-20230523163155645.png)

  - BusinessException

    ![image-20230523163835990](images/image-20230523163835990.png)

  - SystemException

    ![image-20230523163945347](images/image-20230523163945347.png)

- Variables

  ![image-20230523161502150](images/image-20230523161502150.png)

- Issuccessful

  ~~~vbscript
  in_BusinessException is Nothing and in_SystemException is Nothing
  ~~~

- Is Business Exception

  ~~~vbscript
  in_BusinessException isnot Nothing
  ~~~

- If TransactionItem is a QueueItem

  ~~~vbscript
  in_TransactionItem isNot Nothing AndAlso (in_TransactionItem.GetType is GetType(Uipath.Core.QueueItem))
  ~~~

- Omit `Add transactionlog fields (Success)` before `Log Message (Success)`.

- Omit `Remove transactionlog fields (Success)` after `Log Message (Success)`.

- Omit `Add transactionlog fields (Business Exception)` before `Log Message (Business Exception)`.

- Omit `Remove transactionlog fields (Business Exception)` before `Log Message (Business Exception)`.

  

~~~mermaid
flowchart LR
Issuccessful{Is<br>successful} -->|"True"|TransactionItem{If TransactionItem<br>is a QueueItem}
    TransactionItem --> |True|Settransactionstatus["Set transaction status<br>(Successful)"]
    TransactionItem --> |False|LogMessage["Log Message<br>(Success)"]
    Settransactionstatus --> LogMessage
Issuccessful -->|False|IsBusinessException{Is<br>Business Exception}    
    IsBusinessException -->|"True"|TransactionItem1{If TransactionItem<br> is a QueueItem}
        TransactionItem1 --> |True|Settransactionstatus1["Set transaction status<br> (Business Exception status)"]
        TransactionItem1 --> |False|LogMessage1["Log Message<br>(Business Exception)"]
        Settransactionstatus1 --> LogMessage1
    LogMessage --> Assign3[io_TransactionNumber++<br>io_RetryNumber = 0<br>io_ConsecutiveSystemExceptions = 0]
    LogMessage1 --> Assign3
    IsBusinessException -->|"False"|SystemException[System Exception]

~~~
#### System Exception

- QueueRetry

    ~~~vbscript
    in_TransactionItem isNot Nothing AndAlso (in_TransactionItem.GetType is GetType(UiPath.Core.QueueItem))
    ~~~

- Omit `Add transaction log fields (System Exception)` before `Increment consecutive exceptions counter`.

- Omit  `Remove transaction log fields (System Exception)` after  `Invoke RetryCurrentTransaction`.

- When there is an exception in the following 2 try scope, it only prints the warning information instead of throwing it.

~~~mermaid
flowchart LR
subgraph Try2["Try"]
TakeScreenshot[Invoke TakeScreenshot]
end   
TakeScreenshot --> QueueRetry{QueueRetry?}
    QueueRetry --> |True|Settransactionstatus2["Set transaction status<br>(System Exception)"]
        subgraph Try["Retry - RetryNumberSetTransactionStatus"]
            direction TB
            Settransactionstatus2 --> Assignio_RetryNumber[Assign<br>in_TransactionItem.RetryNo<br>to io_RetryNumber]
        end
        Assignio_RetryNumber --> io_ConsecutiveSystemExceptions[io_ConsecutiveSystemExceptions++]  
        io_ConsecutiveSystemExceptions --> InvokeRetryCurrentTransaction[Invoke<br> RetryCurrentTransaction] 
        subgraph Try1["Try"]
        CloseAllApplications[Invoke<br>CloseAllApplications]
        end        
        InvokeRetryCurrentTransaction --> CloseAllApplications      
    QueueRetry --> |False|io_ConsecutiveSystemExceptions

~~~

#### TakeScreenshot

- Arguments

  ![image-20230523164305008](images/image-20230523164305008.png)

- Variables

  Empty

Default Screenshot Path:

~~~
Path.Combline(in_Config("ExScreenshotsFolderPath").ToString, "ExceptionScreenshot_"+Now.ToString("yyMMdd.hhmmss")+".png")
~~~

#### RetryCurrentTransaction

- Arguments

  ![image-20230523215706688](images/image-20230523215706688.png)

- Variables: Empty

- Retry transaction?

  ~~~vb
  Convert.ToInt32(in_Config("MaxRetryNumber"))>0
  ~~~

- Max retries reached?

  ~~~vb
  io_RetryNumber >= Convert.ToInt32(in_Config("MaxRetryNumber"))
  ~~~

- Use Orchestrator's retry?

  ~~~vb
  in_QueueRetry
  ~~~

~~~mermaid
flowchart LR
Retrytransaction{Retry<br> transaction?} --> |Yes|Maxretriesreached{Max retries<br> reached?}
	Maxretriesreached --> |Yes|LogMessageMaxretriesreached["Log message<br> (Max retries reached)"]
		LogMessageMaxretriesreached --> io_RetryNumber[io_RetryNumber=0]
		io_RetryNumber --> io_TransactionNumber[io_TransactionNumber++]
	Maxretriesreached --> |No|LogMessageRetry["Log message<br> (Retry)"]
		LogMessageRetry --> UseOrchestrator{Use<br>Orchestrator's<br>retry?} 
			UseOrchestrator --> |Yes|io_TransactionNumber
			UseOrchestrator --> |No|io_RetryNumber1[io_RetryNumber++]
Retrytransaction -->|No|LogMessageNoRetry["Log message <br>(No retry)"]
    LogMessageNoRetry --> io_TransactionNumber
~~~




## End Process

~~~mermaid
flowchart LR
subgraph Try["Try"]
CloseAllApplications[Invoke CloseAllApplications]
end

CloseAllApplications --> CatchException{Catch Exception}
CatchException -->|True|KillAllProcesses[Invoke KillAllProcesses]
CatchException -->|False|end1((end))
~~~

### CloseAllApplications

- Arguments： Empty
- Variables: Empty

### KillAllProcesses

- Arguments： Empty
- Variables: Empty
