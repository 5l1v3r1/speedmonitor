<?php
$location = "/var/spool/speedmonitor.db";

$db = new SQLite3($location);

if($db) {
    $json_data = array();

    $arr_label = array();
    $arr_upload = array();
    $arr_download = array();

    $results = $db->query("SELECT upload_speed,download_speed,add_date FROM speed WHERE add_date > date('now','-7 day')");
    while ($row = $results->fetchArray()) {
	$upload = round(floatval($row[0]) / 1000,2);
	$download = round(floatval($row[1]) / 1000,2); // Convert to KBytes
	$time = new DateTime($row[2]);
	
	$labels[] = $time->format("H:i d-m-Y");
	$uploads[] = $upload;
	$downloads[] = $download;
    }
    echo json_encode(array("label" => $labels,"upload" => $uploads,"download" => $downloads));
}

?>