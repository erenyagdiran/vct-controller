(function($) {
    $(document).ready(function() {
        var selector = "h2:contains('Slivers')";
        $(selector).parent().addClass("collapsed");
        $(selector).append(" (<a class=\"collapse-toggle\" id=\"slivercollapser\" href=\"#\">Show</a>)");
        $("#slivercollapser").click(function(e) {
            $(selector).parent().toggleClass("collapsed");
            if ($(selector).children().text() == 'Show') {
                $(selector).children().text('Hide');
            } else {
                $(selector).children().text('Show');
            }
            e.preventDefault();
        });
    });
})(django.jQuery);

