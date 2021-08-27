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



function add_copyright_meta_link() {
  $queries = array();
  parse_str($_SERVER['QUERY_STRING'], $queries);
  $es_image_url = 'https://ortana-test.s3.us-east-2.amazonaws.com/stripes/US/' . $queries['state'] . '.png';

  echo( '<title>Result - earthstripes.org</title>
<meta name="description" content="Lorem ipsum dolor sit amet, consectetur."/>
<meta name="robots" content="index, follow, max-snippet:-1, max-video-preview:-1, max-image-preview:large"/>
<link rel="canonical" href="https://earthstripes.org/result/" />
<meta property="og:locale" content="en_US" />
<meta property="og:type" content="article" />
<meta property="og:title" content="Result - earthstripes.org" />
<meta property="og:description" content="Lorem ipsum dolor sit amet, consectetur." />
<meta property="og:url" content="https://earthstripes.org/result/?state=FL&country=US" />
<meta property="og:site_name" content="earthstripes.org" />
<meta property="og:updated_time" content="2021-08-25T21:55:07+00:00" />
<meta property="og:image" content="' . $es_image_url . '" />
<meta property="og:image:secure_url" content="' . $es_image_url . '" />
<meta property="og:image:alt" content="Result" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Result - earthstripes.org" />
<meta name="twitter:description" content="Lorem ipsum dolor sit amet, consectetur." />
<meta name="twitter:image" content="' . $es_image_url . '" />' );
}

add_action( 'wp_head', 'add_copyright_meta_link' );

add_action( 'wp_head', function(){
	if( is_page('52')) {
		remove_all_actions( 'rank_math/head' );
		add_action( 'wp_head', '_wp_render_title_tag', 2 );
	}
}, 1 );