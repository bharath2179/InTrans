#! /bin/sh
inrix_api_base_url="http://api.inrix.com/Traffic/Inrix.ashx"
inrix_vendor_id=1639145093
inrix_consumer_id="2bef7cec‐5104‐4c12‐b946‐693cb7498d54"
download_dir="/lss/research/itrns-otohpc/bharath/dump/"
expiration_time=0
data_download_freq=60

        if [ "$(date +"%s")" -gt $expiration_time ]
        then
                echo "fetching new authentication token"
                # authetication and expiration request
                #inrix_auth_token_url="$inrix_api_base_url?action=getsecuritytoken&Vendorid=${inrix_vendor_id}&consumerid=${inrix_consumer_id}"
                inrix_auth_token_url="http://api.inrix.com/Traffic/Inrix.ashx?action=getsecuritytoken&Vendorid=1639145093&consumerid=2bef7cec-5104-4c12-b946-693cb7498d54"
                 echo $inrix_auth_token_url
                curl -s -o inrix_auth_token_respone.xml $inrix_auth_token_url
                inrix_auth_token=$(xmlstarlet sel -t -v "/Inrix/AuthResponse/AuthToken" inrix_auth_token_respone.xml)
                 echo $inrix_auth_token
                expiration_time=$(xmlstarlet sel el -t -v "/Inrix/AuthResponse/AuthToken/@expiry" inrix_auth_token_respone.xml)
                expiration_time=$(date -d  "${expiration_time}" +'%s')
                 echo $expiration_time
        fi
        inrix_raw_data_url="http://api.inrix.com/Traffic/Inrix.ashx?action=getsegmentspeedingeography&geoid=249&SpeedOutputFields=Speed,Average,Reference,Score,TTM,Confidence&token=${inrix_auth_token}"
         echo "${inrix_raw_data_url}"
        curl -s -o "${download_dir}$(date +"%b-%d-%Y")/`date '+%Y_%m_%d_%H_%M_%S'`.xml" --create-dirs $inrix_raw_data_url
