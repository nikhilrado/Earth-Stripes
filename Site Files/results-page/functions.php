<?php
/**
 * Theme functions and definitions
 *
 * @package HelloElementorChild
 */

/**
 * Load child theme css and optional scripts
 *
 * @return void
 */
function hello_elementor_child_enqueue_scripts() {
	wp_enqueue_style(
		'hello-elementor-child-style',
		get_stylesheet_directory_uri() . '/style.css',
		[
			'hello-elementor-theme-style',
		],
		'1.0.0'
	);
}
add_action( 'wp_enqueue_scripts', 'hello_elementor_child_enqueue_scripts', 20 );

function generate_custom_meta_tags() {
	//returns the url that this page should be (reorders, and removes extra query params ig)
	function get_results_canonical_URL() {
		$queries = array();
		parse_str($_SERVER['QUERY_STRING'], $queries);
		$es_canonical_url = 'https://www.earthstripes.org/result/?country=' . $queries['country'];
		if( !is_null($queries['state'])) {
			$es_canonical_url = $es_canonical_url . '&state=' . $queries['state'];
		};
		if( !is_null($queries['county'])) {
			$es_canonical_url = $es_canonical_url . '&county=' . $queries['county'];
		};
		return($es_canonical_url);
	}

	function get_resource_id(){
		$queries = array();
		parse_str($_SERVER['QUERY_STRING'], $queries);
		$resource_id = 'https://ortana-test.s3.us-east-2.amazonaws.com/stripes/' . $queries['country'];
		if( !is_null($queries['state'])) {
			$resource_id = $resource_id . '/' . $queries['state'];
		};
		if( !is_null($queries['county'])) {
			$resource_id = $resource_id . '/' . $queries['county'] . "+" . $queries['state'];
		};
		$resource_id = str_replace(" ","+",$resource_id);
		return($resource_id . '.png');
	}

	function state_code_to_state($state_code){
		$state_code_array = array("ty","DC","AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY");
		$states_array = array("County","Washington D.C.","Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming");
		return($states_array[array_search($state_code, $state_code_array)]);
	}

	function country_code_to_state($country_code){
		$country_code_array = array("AF","AX","AL","DZ","AS","AD","AO","AI","AQ","AG","AR","AM","AW","AU","AT","AZ","BS","BH","BD","BB","BY","BE","BZ","BJ","BT","BO","BQ","BA","BW","BR","IO","BG","BF","MM","BI","KH","CM","CA","CV","KY","CF","TD","CL","CN","CX","CO","KM","CG","CD","CR","CI","HR","CU","CW","CY","CZ","DK","DJ","DM","DO","EC","EG","SV","GQ","ER","EE","ET","FK","FO","FJ","FI","FR","GF","PF","TF","GA","GM","GE","DE","GH","GR","GL","GD","GP","GU","GT","GG","GN","GW","GY","HT","HM","HN","HK","HU","IS","IN","ID","IR","IQ","IE","IM","IL","IT","JM","JP","JE","JO","KZ","KE","KI","KW","KG","LA","LV","LB","LS","LR","LY","LI","LT","LU","MO","MK","MG","MW","MY","ML","MT","MQ","MR","MU","YT","MX","MD","MC","MN","ME","MS","MA","MZ","NA","NP","NL","NC","NZ","NI","NE","NG","NU","KP","MP","NO","OM","PK","PW","PS","PA","PG","PY","PE","PH","PL","PT","PR","QA","RE","RO","RU","RW","BL","KN","LC","MF","PM","VC","WS","SM","ST","SA","SN","RS","SC","SL","SG","SX","SK","SI","SB","SO","ZA","GS","KR","ES","LK","SD","SR","SJ","SZ","SE","CH","SY","TW","TJ","TZ","TH","TL","TG","TO","TT","TN","TR","TM","TC","UG","UA","AE","GB","US","UY","UZ","VE","VN","VG","EH","YE","ZM","ZW");
		$countries_array = array("Afghanistan","Åland","Albania","Algeria","American Samoa","Andorra","Angola","Anguilla","Antarctica","Antigua and Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bonaire, Saint Eustatius and Saba","Bosnia and Herzegovina","Botswana","Brazil","British Virgin Islands","Bulgaria","Burkina Faso","Burma","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","China","Christmas Island","Colombia","Comoros","Congo","Congo (Democratic Republic of the)","Costa Rica","Côte d'Ivoire","Croatia","Cuba","Curaçao","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Falkland Islands (Islas Malvinas)","Faroe Islands","Fiji","Finland","France (Europe)","French Guiana","French Polynesia","French Southern and Antarctic Lands","Gabon","Gambia","Georgia","Germany","Ghana","Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guernsey","Guinea","Guinea-Bissau","Guyana","Haiti","Heard Island and McDonald Islands","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kiribati","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Mali","Malta","Martinique","Mauritania","Mauritius","Mayotte","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands (Europe)","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Niue","North Korea","Northern Mariana Islands","Norway","Oman","Pakistan","Palau","Palestina","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Barthélemy","Saint Kitts and Nevis","Saint Lucia","Saint Martin","Saint Pierre and Miquelon","Saint Vincent and the Grenadines","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Sint Maarten","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","South Georgia and the South Sandwich Isla","South Korea","Spain","Sri Lanka","Sudan","Suriname","Svalbard and Jan Mayen","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor-Leste","Togo","Tonga","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Turks and Caicas Islands","Uganda","Ukraine","United Arab Emirates","United Kingdom (Europe)","United States","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands","Western Sahara","Yemen","Zambia","Zimbabwe");
		return($countries_array[array_search($country_code, $country_code_array)]);
	}
	
	function get_location_name(){
		$queries = array();
		parse_str($_SERVER['QUERY_STRING'], $queries);
		$countries_with_subdivistions = array(NULL,"US");
		if(! in_array($queries['country'],$countries_with_subdivistions)){
			return(country_code_to_state($queries['country']));
		};
		if(is_null($queries['county'])){
			return(state_code_to_state($queries['state'])); //. ", " . $queries['country']);
		};
		if(! is_null($queries['county'])){
			return($queries['county'] . ", " . state_code_to_state($queries['state']));
		};
	}

	
	$es_image_url = get_resource_id();
	$es_canonical_url = get_results_canonical_URL();
	$es_location_name = get_location_name();
	$es_title_name = $es_location_name . ' - EarthStripes.org';
	$es_image_alt = 'Warming Stripes for ' . $es_location_name;
	$es_description_name = 'See how temperature is changing in ' . $es_location_name . ' and how climate change is impacting our communities.';
	echo( '<title>' . $es_title_name . '</title>
<meta name="description" content="' . $es_description_name . '"/>
<meta name="robots" content="index, follow, max-snippet:-1, max-video-preview:-1, max-image-preview:large"/>
<link rel="canonical" href="' . $es_canonical_url . '" />
<meta property="og:locale" content="en_US" />
<meta property="og:type" content="article" />
<meta property="og:title" content="' . $es_title_name . '" />
<meta property="og:description" content="' . $es_description_name . '" />
<meta property="og:url" content="' . $es_canonical_url . '" />
<meta property="og:site_name" content="Earth Stripes" />
<meta property="og:updated_time" content="2021-08-25T21:55:07+00:00" />
<meta property="og:image" content="' . $es_image_url . '" />
<meta property="og:image:secure_url" content="' . $es_image_url . '" />
<meta property="og:image:alt" content="' . $es_image_alt . '" />
<meta name="twitter:site" content="@earthstripes" />
<meta name="twitter:creator" content="@nikhilrado" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="' . $es_title_name . '" />
<meta name="twitter:description" content="' . $es_description_name . '" />
<meta name="twitter:image" content="' . $es_image_url . '" />
<meta property="snap:sticker" content="' . $es_image_url . '" />

'
);
}

add_action( 'wp_head', 'generate_custom_meta_tags' );

add_action( 'wp_head', function(){
	if( is_page('52')) {
		remove_all_actions( 'rank_math/head' );
		//add_action( 'wp_head', '_wp_render_title_tag', 2 );
	}
}, 1 );