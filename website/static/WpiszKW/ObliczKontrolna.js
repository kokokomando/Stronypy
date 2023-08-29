
    const wagi = [1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7];

    const slownik_znakow = {
      '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
      '6': 6, '7': 7, '8': 8, '9': 9,
      'X': 10, 'A': 11, 'B': 12, 'C': 13, 'D': 14,
      'E': 15, 'F': 16, 'G': 17, 'H': 18, 'I': 19,
      'J': 20, 'K': 21, 'L': 22, 'M': 23, 'N': 24,
      'O': 25, 'P': 26, 'R': 27, 'S': 28, 'T': 29,
      'U': 30, 'W': 31, 'Y': 32, 'Z': 33
    };

    function calculateKontrolna() {
      const input1 = document.getElementById('input1').value;
      const input2 = document.getElementById('input2').value;
	
	

      const kwtest = input1 + input2;
      const KW2 = kwtest.replace("/", "");

      const char_list = Array.from(KW2);

      const replaced_list = char_list.map(char => slownik_znakow[char] !== undefined ? slownik_znakow[char] : char);

      const numbers = replaced_list;

      const multiplied_list = numbers.map((num, index) => num * wagi[index % wagi.length]);

      const total = multiplied_list.reduce((sum, value) => sum + value, 0);

      const kontrolna = total % 10;

      document.getElementById('result').textContent = "Cyfra Kontrolna to: " + kontrolna;
    }
