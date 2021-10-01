// Functions that get executed only after the DOM's content has finished loading
document.addEventListener('DOMContentLoaded', function() {

    // Get the submit button element
    let submit = document.querySelector('#btn1');

    // Question 1's input
    let text_input = document.getElementById('q1');

    // Question 2's input
    let email_input = document.getElementById('q2');

    // Question 3's inputs
    let ans1 = document.getElementById('answer-1');
    let ans2 = document.getElementById("answer-2");
    let ans3 = document.getElementById("answer-3");

    // Question 4's inputs
    var items = new Array(4);
    items[0] = document.getElementById('item-1');
    items[1] = document.getElementById('item-2');
    items[2] = document.getElementById('item-3');
    items[3] = document.getElementById('item-4');

    // Run the function every time the submit button is clicked
    submit.addEventListener('click', function() {

        // Check Q1
        if (text_input.value) {
            document.getElementById('response-question-1').innerHTML = 'Your answer to question 1: ' + text_input.value;
        }
        else {
            document.getElementById('response-question-1').innerHTML = 'You have not yet answered question 1.';
        }

        // Check Q2
        if (email_input.value) {
            document.getElementById('response-question-2').innerHTML = 'Your answer to question 2: ' + email_input.value;
        }
        else {
            document.getElementById('response-question-2').innerHTML = 'You have not yet answered question 2.';
        }

        // Check Q3
        if (ans1.checked) {
            document.getElementById('response-question-3').innerHTML = 'You have chosen ' + ans1.value + ' for question 3.';
        }
        else if (ans2.checked) {
            document.getElementById('response-question-3').innerHTML = 'You have chosen ' + ans2.value + ' for question 3.';
        }
        else if (ans3.checked) {
            document.getElementById('response-question-3').innerHTML = 'You have chosen ' + ans3.value + ' for question 3.';
        }
        else {
            document.getElementById('response-question-3').innerHTML = 'You have not yet chosen an answer to question 3.';
        }

        // Check Q4
        var checked = false;
        var responses = [];
        for (var i = 0; i < 4; i++) {
            if (items[i].checked) {
                checked = true;
                responses.push(items[i].value);
            }
        }

        if (checked) {
            document.getElementById('response-question-4').innerHTML = 'You have selected ' + responses.join(', ') + ' for question 4.';
        }

        else if (!checked) {
            document.getElementById('response-question-4').innerHTML = 'You have not yet selected any item for question 4.';
        }
    })
})