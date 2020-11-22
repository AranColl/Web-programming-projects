async function delete_loan(loan_id){
    const button = document.getElementById("delete_button" + loan_id);

    await fetch(`../delete_loan/${loan_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            loan: loan_id
        })
    });
    var div = document.getElementById("loan" + loan_id);;
    div.parentNode.removeChild(div);
}