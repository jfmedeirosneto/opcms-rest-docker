(function ($) {
    "use strict"; // Start of use strict
    // Get data of main site 1
    $(document).ready(function () {
        $.ajax({
            url: "../sites/public/1"
        }).then(function (site_data) {
            // Site Data
            $(document).attr("title", site_data.site_title);
            $('meta[name="description"]').attr('content', site_data.site_description.replace(/\n/g, '\u00A0'));
            $('meta[name="author"]').attr('content', site_data.owner_name);
            $('#site-title-a').text(site_data.site_title);
            $('#site-title-h1').text(site_data.site_title);
            $('#site-description-p').html(site_data.site_description.replace(/\n/g, '<br/>'));
            $('#site-copyright-div').text(site_data.site_copyright);

            // Page Data
            $('#page-title-a').text(site_data.page_title);
            $('#page-title-h2').text(site_data.page_title);
            $('#page-content-p').html(site_data.page_content.replace(/\n/g, '<br/>'));

            // Owner Data
            $('#owner-name-h3').text(site_data.owner_name);
            $('#owner-address-p').html(site_data.owner_address.replace(/\n/g, '<br/>'));
            $('#owner-map-url-a').text(site_data.owner_map_url);
            $('#owner-map-url-a').attr("href", site_data.owner_map_url);
            $.each(site_data.owner_phones, function (index, value) {
                $('#owner-phones-div').append(
                    '<a class="d-block mb-3" href="tel:' + value + '">' + value + '</a>'
                );
            });
            $.each(site_data.owner_whatsapp_phones, function (index, value) {
                var whatsapp_number = parseInt(value.replace(/[^0-9]/g, ''), 10);
                $('#owner-whatsapp-phones-div').append(
                    '<a class="d-block mb-3" href="https://wa.me/' + whatsapp_number + '">' + value + '</a>'
                );
            });
            $('#owner-email-a').text(site_data.owner_email);
            $('#owner-email-a').attr("href", 'mailto:' + site_data.owner_email);
            $('#owner-facebook-url-a').text(site_data.owner_facebook_url);
            $('#owner-facebook-url-a').attr("href", site_data.owner_facebook_url);
            $('#owner-twitter-url-a').text(site_data.owner_twitter_url);
            $('#owner-twitter-url-a').attr("href", site_data.owner_twitter_url);
            $('#owner-instagram-url-a').text(site_data.owner_instagram_url);
            $('#owner-instagram-url-a').attr("href", site_data.owner_instagram_url);

            // Reveal document.body
            $(document.body).fadeIn(2500);
        });

        // Get data of portfolios
        $.ajax({
            url: "../portfolios/public"
        }).then(function (portfolios_data) {
            //Create template data
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

            //Load template
            $("#portfolio-target").loadTemplate($("#portfolio-template"),template_data);
        });
    });
})(jQuery); // End of use strict
