<?php

include('../vendor/autoload.php');
use Telegram\Bot\Api;

include('rb.php');
R::setup( 'mysql:host=localhost;dbname=u0530515_echobot', 'u0530515_echobot', '0S8x8I3y' );

$address = 'Mxf40755bf5e19dd55e1b81e8edc4d16c982b255a1';

$transactions = json_decode(file_get_contents('https://explorer-api.apps.minter.network/api/v1/addresses/'.$address.'/transactions'), true);
$transactions = $transactions['data'];

foreach ($transactions as $key => $value) {

	$haystack = file_get_contents('data');
	$pos = stripos($haystack, $value['hash']);
	if ($pos === false) {
	    $haystack = $haystack.$value['hash'];
	    file_put_contents('data', $haystack);
	} else {
	    continue;
	}

    $transaction = json_decode(file_get_contents('https://api.minter.stakeholder.space/transaction?hash='.$value['hash']), true);

    $subj = $transaction['result']['payload'];
    $subj = base64_decode($subj);

    if ($value['data']['coin'] != 'LAPKINLAB') {
        continue;
    }

    if ($value['data']['to'] != $address) {
        continue;
    }

    if ($subj{1} == ":" && (float)$value['data']['value'] >= (float)1) {

        $presubj = mb_strtolower($subj);
        if ($presubj{0} == "n") {
            $wname = R::findOne( 'names', ' wallet = ? ', [ $value['from'] ] );
            if ($wname) {
                $wname->name = trim(substr($subj, 2));
                R::store( $wname );
            } else {
                $wname = R::dispense( 'names' );
                $wname->wallet = $value['from'];
                $wname->name = trim(substr($subj, 2));
                $wname->status = "DLT";
                $wname->namestyle = "DLT";
                $wname->statusstyle = "DLT";
                R::store( $wname );
            }
            continue;
        } elseif ($presubj{0} == "s") {
            $wname = R::findOne( 'names', ' wallet = ? ', [ $value['from'] ] );
            if ($wname) {
                $wname->status = trim(substr($subj, 2));
                R::store( $wname );
            } else {
                $wname = R::dispense( 'names' );
                $wname->wallet = $value['from'];
                $wname->name = "DLT";
                $wname->status = trim(substr($subj, 2));
                $wname->namestyle = "DLT";
                $wname->statusstyle = "DLT";
                R::store( $wname );
            }
            continue;
        }

    }

    $telegram = new Api('853346470:AAF1HvHrBC8em7jyjKM0ZRZ8Bx1ppiV35SY');
    $chat_id = -1001430008437;
    //$chat_id = 604616538;

    $icon = file_get_contents('https://minterscan.pro/addresses/'.$value['from'].'/icon');

    $delegations = json_decode(file_get_contents('https://explorer-api.apps.minter.network/api/v1/addresses/'.$value['from'].'/delegations'), true);
    $delegations = $delegations['data'];

    foreach ($delegations as $ckey => $cvalue) {
        if ($cvalue['coin'] == 'LAPKINLAB') {
            $min = 0.5;
            break;
        }
    }

    if ($min != 0.5 && $min != 0.25) {
        $min = 1;
    }

    $wname = R::findOne( 'names', ' wallet = ? ', [ $value['from'] ] );

    $subj = str_replace("_", "\_", $subj);
    $name = str_replace("_", "\_", $wname['name']);
    $status = str_replace("_", "\_", $wname['status']);

    /*$subj = str_replace("#", "\#", $subj);
    $name = str_replace("#", "\#", $wname['name']);
    $status = str_replace("#", "\#", $wname['status']);*/

    if (findv($subj, "https") || findv($subj, "http") || findv($subj, ".ru") || findv($subj, ".com") || findv($subj, "@")) {} else {
    	$min = 0.25;
    }

    if ($name == "" || $name == "DLT") {
        $name = substr($value['from'],0,6)."...".$newstring = substr($value['from'], -4);
    }
    if ($status == "" || $status == "DLT") {
        $status = "";
    } else {
        $status = "        ".$status."\n";
    }

    if ((float)$value['data']['value'] >= (float)$min) {
            $reply = $icon." [".$name."](https://minterscan.net/address/".$value['from'].")
".$status."
``".$subj."``

[".(float)$value['data']['value']." LAPKINLAB](https://explorer.minter.network/transactions/".$value['hash'].")";

    		$getcon = file_get_contents("https://api.comments.bot/createPost?api_key=22ed0fadf5be0bd7b53cdef327a78b11&owner_id=161799016&type=text&text=Voice%20of%20minter&parse_mode=Markdown&administrators=604616538,420090286,161799016");

    		$getcon = json_decode($getcon, true);

    		$skeyboard = json_encode([
		        'inline_keyboard'=>[
		            [
		                ['text'=>'Комментарии', 'url'=> $getcon['result']['link']]
		            ]
		        ]
		    ]);

            $message = $telegram->sendMessage([ 'parse_mode' => 'Markdown', 'disable_web_page_preview' => 1, 'chat_id' => $chat_id, 'text' => $reply, 'reply_markup' => $skeyboard ]);
            $messages = json_decode(file_get_contents("../public_html/message_data"), true);
            $messages_new_tx = array('text' => $subj, 'name' => $name, 'from' => $value['from'], 'status' => $status, 'summ' => $value['data']['value'], 'hash' => $value['hash'], 'comments' => $getcon['result']['link']);
            $messages[count($messages)] = $messages_new_tx;
            file_put_contents("../public_html/message_data", json_encode($messages));
    }

}

function findv($string, $v)
{
	$pos = strripos($string, $v);

	if ($pos === false) {
	    return 0;
	} else {
	    return 1;
	}
}

?>