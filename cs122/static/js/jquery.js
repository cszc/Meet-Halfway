//This script enables the css loader. Actual css is in css directory and
//borrowed from https://github.com/ConnorAtherton/loaders.css/tree/master
//The script below is custom written.
$('#part2-form').on('submit', function() {
    $('.loader-outer, #part2-container').toggleClass('hidden');
});

// This script enables the fairness score tooltip to display on the results page.
// Taken from http://getbootstrap.com/javascript/#tooltips
$('[data-toggle="tooltip"]').tooltip()
