(function ($) {
    'use strict'; // Start of use strict
    $(document).ready(function () {
        // Load data asynchronous
        $.when(
            $.ajax('../sites/public/1'),
            $.ajax('../portfolios/public')
        ).done(function (ajax1_response, ajax2_response) {
            // Site and portfolios data
            var site_data = ajax1_response[0];
            var portfolios_data = ajax2_response[0];

            // Site data
            $(document).attr('title', site_data.site_title);
            $('meta[name="description"]').attr('content', site_data.site_description.replace(/\n/g, '\u00A0'));
            $('meta[name="author"]').attr('content', site_data.owner_name);
            $('#site-title-a').text(site_data.site_title);
            $('#site-title-h1').text(site_data.site_title);
            $('#site-description-p').html(site_data.site_description.replace(/\n/g, '<br/>'));
            $('#site-copyright-div').text(site_data.site_copyright);

            // Page data
            $('#page-title-a').text(site_data.page_title);
            $('#page-title-h2').text(site_data.page_title);
            $('#page-content-p').html(site_data.page_content.replace(/\n/g, '<br/>'));

            // Create owner template data
            var owner_phones_template_data = [];
            $.each(site_data.owner_phones, function (index, value) {
                owner_phones_template_data.push({
                    'href': 'tel:' + value,
                    'content': value
                });
            });
            var whatsapp_phones_template_data = [];
            $.each(site_data.owner_whatsapp_phones, function (index, value) {
                var whatsapp_number = parseInt(value.replace(/[^0-9]/g, ''), 10);
                whatsapp_phones_template_data.push({
                    'href': 'https://wa.me/' + whatsapp_number,
                    'content': value
                });
            });

            // Owner data
            $('#owner-name-h3').text(site_data.owner_name);
            $('#owner-address-p').html(site_data.owner_address.replace(/\n/g, '<br/>'));
            $('#owner-map-url-a').text(site_data.owner_map_url);
            $('#owner-map-url-a').attr('href', site_data.owner_map_url);
            $('#owner-phones-div').loadTemplate($('#contact-link-template'), owner_phones_template_data);
            $('#owner-whatsapp-phones-div').loadTemplate($('#contact-link-template'), whatsapp_phones_template_data);
            $('#owner-email-a').text(site_data.owner_email);
            $('#owner-email-a').attr('href', 'mailto:' + site_data.owner_email);
            $('#owner-facebook-url-a').text(site_data.owner_facebook_url);
            $('#owner-facebook-url-a').attr('href', site_data.owner_facebook_url);
            $('#owner-twitter-url-a').text(site_data.owner_twitter_url);
            $('#owner-twitter-url-a').attr('href', site_data.owner_twitter_url);
            $('#owner-instagram-url-a').text(site_data.owner_instagram_url);
            $('#owner-instagram-url-a').attr('href', site_data.owner_instagram_url);

            // Create portfolios template data
            var template_data = [];
            $.each(portfolios_data, function (index, portfolio_data) {
                $.each(portfolio_data.pictures, function (index, picture_data) {
                    template_data.push({
                        'category': portfolio_data.category,
                        'project_name': portfolio_data.project_name,
                        'fullsize_url': picture_data.fullsize_url,
                        'thumbnail_url': picture_data.thumbnail_url,
                    });
                });
            });

            //Load portfolios template
            $('#portfolio-target').loadTemplate($('#portfolio-template'), template_data);

            // Reveal document.body
            $(document.body).fadeIn(2500);
        }).fail(function () {
            alert('Error on loading site data');
        });
    });
})(jQuery); // End of use strict
