(function ($) {
    "use strict"; // Start of use strict
    // Get data of main site
    $(document).ready(function () {
        $.ajax({
            url: "../sites/public/1"
        }).then(function (data) {
            // Site Data
            $(document).attr("title", data.site_title);
            $('meta[name="description"]').attr('content', data.site_description.replace(/\n/g, '\u00A0'));
            $('meta[name="author"]').attr('content', data.owner_name);
            $('#site-title-a').text(data.site_title);
            $('#site-title-h1').text(data.site_title);
            $('#site-description-p').html(data.site_description.replace(/\n/g, '<br/>'));
            $('#site-copyright-div').text(data.site_copyright);

            // Page Data
            $('#page-title-a').text(data.page_title);
            $('#page-title-h2').text(data.page_title);
            $('#page-content-p').html(data.page_content.replace(/\n/g, '<br/>'));

            // Owner Data
            $('#owner-name-h3').text(data.owner_name);
            $('#owner-address-p').html(data.owner_address.replace(/\n/g, '<br/>'));
            $('#owner-map-url-a').text(data.owner_map_url);
            $('#owner-map-url-a').attr("href", data.owner_map_url);
            $.each(data.owner_phones, function (index, value) {
                $('#owner-phones-div').append(
                    '<a class="d-block mb-3" href="tel:' + value + '">' + value + '</a>'
                );
            });
            $.each(data.owner_whatsapp_phones, function (index, value) {
                var whatsapp_number = parseInt(value.replace(/[^0-9]/g, ''), 10);
                $('#owner-whatsapp-phones-div').append(
                    '<a class="d-block mb-3" href="https://wa.me/' + whatsapp_number + '">' + value + '</a>'
                );
            });
            $('#owner-email-a').text(data.owner_email);
            $('#owner-email-a').attr("href", 'mailto:' + data.owner_email);
            $('#owner-facebook-url-a').text(data.owner_facebook_url);
            $('#owner-facebook-url-a').attr("href", data.owner_facebook_url);
            $('#owner-twitter-url-a').text(data.owner_twitter_url);
            $('#owner-twitter-url-a').attr("href", data.owner_twitter_url);
            $('#owner-instagram-url-a').text(data.owner_instagram_url);
            $('#owner-instagram-url-a').attr("href", data.owner_instagram_url);

            // Reveal document.body
            $(document.body).fadeIn(2500);
        });
    });
})(jQuery); // End of use strict
