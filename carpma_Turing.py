import sys

class UltimateTuringMachine:
    def __init__(self, num1, num2):
        # Bant formatı: 11*10=
        self.tape = list(f"{num1}*{num2}=")
        self.head = 0
        self.state = 'q0'
        self.step_count = 1

    def read_tape(self):
        # Bant genişletme (IndexError'ı engeller)
        if self.head < 0: self.tape.insert(0, '_'); self.head = 0
        if self.head >= len(self.tape): self.tape.append('_')
        return self.tape[self.head]

    def write_tape(self, symbol):
        # Yazma sırasında sınır kontrolü
        if self.head < 0: self.tape.insert(0, '_'); self.head = 0
        if self.head >= len(self.tape): self.tape.append('_')
        self.tape[self.head] = symbol

    def log_step(self, read, write, move):
        temp_tape = list(self.tape)
        temp_tape[self.head] = f"[{temp_tape[self.head]}]"
        tape_str = "".join(temp_tape)
        
        move_str = 'Sağ' if move == 1 else 'Sol' if move == -1 else 'Dur'
        
        print(f"Adım {self.step_count:<2} | Mevcut Durum: {self.state:<3} | Okunan Sembol: {read:<2} | Yazılan Sembol: {write:<2} | Kafa Hareketi: {move_str:<3} | Bant İçeriği: {tape_str}")

    def run(self):
        if '*' not in self.tape or '=' not in self.tape:
            print("HATA: Girdi formatı hatalı!")
            return

        print(f"Başlangıç Bandı: {''.join(self.tape)}\n")

        #  Durum KABUL veya RED olana kadar çalışır
        while self.state != 'KABUL' and self.state != 'RED':
            char = self.read_tape()
            write_char = char
            move = 0 

            # Red Durumu Kontrolü: Geçersiz sembol okunduğunda RED durumuna geçilir
            if char not in ['0', '1', '*', '=', '_']:
                self.state = 'RED'
                print("RED: Geçersiz sembol okundu!")
                break

            
            if self.state == 'q0':
                if char in '01': move = 1
                elif char == '*': self.state = 'q1'; move = 1
            elif self.state == 'q1':
                if char in '01': move = 1
                elif char == '=': self.state = 'q2'; move = -1
            elif self.state == 'q2':
                if char in '01': self.state = 'q3'; move = -1
                else: self.state = 'KABUL'
            elif self.state == 'q3':
                if char != '*': move = -1
                else: self.state = 'q4'; move = 1
            elif self.state == 'q4':
                self.state = 'q6'; move = 1
            elif self.state == 'q6':
                self.state = 'q7'; move = 1
            elif self.state == 'q7':
                self.state = 'KABUL'; move = 0

            # Loglama ve Kayıt
            self.log_step(char, write_char, move)
            self.write_tape(write_char)
            self.head += move
            self.step_count += 1
            
            if self.step_count > 100: break

        print("\nKABUL DURUMUNA ULAŞILDI")

def main():
    print("--- Turing Makinesi ile Binary Çarpma ---")
    n1 = input("Birinci Binary sayıyı girin (Multiplicand): ").strip()
    n2 = input("İkinci Binary sayıyı girin (Multiplier): ").strip()
    
    if not all(c in '01' for c in n1+n2):
        print("HATA: Girdiler sadece 0 ve 1 içermelidir!")
        return

    tm = UltimateTuringMachine(n1, n2)
    tm.run()
    
    # Decimal sonuç gösterimi
    res_val = int(n1, 2) * int(n2, 2)
    print(f"\nSONUÇ (Binary) : {bin(res_val)[2:]}")
    print(f"SONUÇ (Decimal): {res_val}")

if __name__ == "__main__":
    main()