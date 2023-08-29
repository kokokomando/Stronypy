

function addLeadingZeros() {
    let inputValue = input2.value;
    const minLength = 8;

    if (inputValue.length < minLength) {
        const paddingCount = minLength - inputValue.length;
        const padding = "0".repeat(paddingCount);
        inputValue = padding + inputValue;
        input2.value = inputValue;
    }
    // Call calculateKontrolna() here if needed
}
