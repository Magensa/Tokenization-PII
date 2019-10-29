#!/usr/bin/env python3.7
import requests
import os 
from typing import NamedTuple
from MagtekTokenizationWebService import pfxtopemutil

class RedeemTokensRequest(NamedTuple):
    """Description Of RedeemTokensRequest"""
    customerCode :str
    Password :str
    userName :str
    customerTransactionID :str
    token :str


class RedeemTokens:

    def __init__(self,redeemTokensRequest): 
        self.__redeemTokensRequest = redeemTokensRequest


    def CallService(self,webServiceUrl,certificateFileName,certificatePassword):
        soapRequest = f"""
       <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tok="http://www.magensa.net/Token/" xmlns:tok1="http://schemas.datacontract.org/2004/07/TokenWS.Core" xmlns:sys="http://schemas.datacontract.org/2004/07/System.Collections.Generic">
  <soapenv:Header/>
  <soapenv:Body>
    <tok:RedeemToken>
      <tok:RedeemTokenRequest>
        <tok1:AdditionalRequestData>
          <sys:KeyValuePairOfstringstring>
            <sys:key></sys:key>
            <sys:value></sys:value>
          </sys:KeyValuePairOfstringstring>
        </tok1:AdditionalRequestData>
        <tok1:Authentication>
          <tok1:CustomerCode>{self.__redeemTokensRequest.customerCode}</tok1:CustomerCode>
          <tok1:Password>{self.__redeemTokensRequest.Password}</tok1:Password>
          <tok1:Username>{self.__redeemTokensRequest.userName}</tok1:Username>
        </tok1:Authentication>
        <tok1:CustomerTransactionID>{self.__redeemTokensRequest.customerTransactionID}</tok1:CustomerTransactionID>
        <tok1:Token>{self.__redeemTokensRequest.token}</tok1:Token>
      </tok:RedeemTokenRequest>
    </tok:RedeemToken>
  </soapenv:Body>
</soapenv:Envelope>  
        """

        headers = {
        "Content-Type": "text/xml;charset=utf-8",
        "Content-Length":  str(len(soapRequest)),
        "SOAPAction": "http://www.magensa.net/Token/ITokenService/RedeemToken"
        }
            
        response = None

        if ((certificateFileName is None) or (certificateFileName.strip() == "")):
            #send soap request without attaching certificate
            response = requests.post(webServiceUrl,data=soapRequest,headers=headers)
        else:
            util = pfxtopemutil.PfxToPemUtility()
            try:
                util.Convert(certificateFileName, certificatePassword) 
                response = requests.post(webServiceUrl, cert=util.tempFileName, data=soapRequest,headers=headers)
            except Exception as ex:
                print(ex)
            finally:
                if ((not util.tempFileName is None) and (os.path.exists(util.tempFileName))):
                    os.remove(util.tempFileName)
        return response



