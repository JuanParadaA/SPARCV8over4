/*
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assembler Code Step Simulator</title>
    <style>
        textarea { width: 100%; }
        pre { background-color: #f0f0f0; padding: 10px; }
        table { width: 100%; }
        th, td { padding: 5px; text-align: left; }
    </style>
</head>
<body>
    <h1>Assembler Code Step Simulator</h1>
    <textarea id="codeInput" rows="15" cols="60">
MOV R1,5
SETHI R2,1048944
LD R3,[R2+28]
SUBcc R1,R1,1
BzC -3
NOP

    </textarea>
    <br>
    <button onclick="step()">Step</button
    <h2>Simulation Output</h2>
    <pre id="output"></pre>
    <h2>Register States</h2>
    <table>
        <thead>
            <tr><th>Register</th><th>Value</th></tr>
        </thead>
        <tbody id="registerTable">
        </tbody>
    </table>

   <div id="memory-container">
        <!--input type="text" id="memory_address" placeholder="Memory Address"/-->
        <div id="backend-switch">
            <label class="switch">
                <input type="checkbox">
                <span class="slider"></span>
            </label>
            <span>Backend</span>
        </div>
    </div>
    
    
    <h2>Memory </h2>
<textarea id="memoryInput" rows="10" cols="60">  </textarea>

    <script>
*/
        const instructions = [
            "ADD", "AND", "OR", "XOR", "SUB", "ANDN", "ORN", "XNOR", "ADDX", "UMUL", "SMUL", "SUBX", "UDIV", "SDIV",
            "ADDcc", "ANDcc", "ORcc", "XORcc", "SUBcc", "ANDNcc", "ORNcc", "XNORcc", "ADDXcc", "UMULcc", "SMULcc", "SUBXcc", "UDIVcc", "SDIVcc",
            "SLL", "SRL", "SRA",
            "LD", "ST",
            "BN", "BE", "BLE", "BL", "BLEU", "BCS", "BNEG", "BVS", "BA", "BNE", "BG", "BGE", "BGU", "BCC", "BPOS", "BVC",
            "CALL", "RETL", "JMPL",
            "SETHI",
            "NOP", "MOV", "CMP", "TST", "NOT", "NEG", "INC", "DEC", "CLR",
            "BnS", "BnC", "BzS", "BzC", "BcS", "BcC", "BvS", "BvC"
        ];

        const registers = { R0: 0, R1: 0, R2: 0, R3: 0, R4: 0, R5: 0, R6: 0, R7: 0 };
        let memory = {};

        let parsed = [];
        let instructionPointer = 0;

        function tokenize(code) {
            return code
                .replace(/,\s*/g, ',') // Remove extra spaces after commas
                .split(/[\s,]+/) // Split by any whitespace
                .filter(token => token.length > 0); // Remove empty tokens
                
        }

        function parse(tokens) {
            const parsed = [];
            let i = 0;

            while (i < tokens.length) {
                const token = tokens[i];

                if (instructions.includes(token)) {
                    const instruction = { op: token };
                    i++;

                    const args = [];
                    while (i < tokens.length && !instructions.includes(tokens[i]) && tokens[i] !== 'NOP') {
                        let arg = tokens[i].replace(/,$/, '');

                        if (arg.startsWith('[') && arg.endsWith(']')) {
                            arg = arg.slice(1, -1); // Remove brackets
                            if (arg.includes('+')) {
                                args.push(`[${arg}]`);
                            } else {
                                args.push(arg);
                            }
                        } else {
                            args.push(arg);
                        }

                        i++;
                    }
                    instruction.args = args;
                    parsed.push(instruction);
                } else {
                    i++;
                }
            }
            return parsed;
        }

        function executeInstruction(instruction) {
            const args = instruction.args.map(arg => {
                if (arg.startsWith('[')) {
                    const parts = arg.slice(1, -1).split('+');
                    const regValue = registers[parts[0]];
                    const offset = parts[1] ? parseInt(parts[1], 10) : 0;
                    return regValue + offset;
                } else if (registers.hasOwnProperty(arg)) {
                    return registers[arg];
                } else {
                    return parseInt(arg, 10);
                }
            });

            switch (instruction.op) {
                case 'MOV':
                    
                    registers[instruction.args[0]] = args[1];
                    break;
                case 'LD':
                    if (!(memory.hasOwnProperty([args[1]]))){
                        memory[args[1]] = parseInt(prompt("Value of memory "+args[1], "0")); 
                    }
                    registers[instruction.args[0]] = memory[args[1]];
                    break;
                case 'ST':
                    memory[args[0]] = args[1];
                    break;
                case 'ADD':
                    registers[instruction.args[0]] = args[1] + args[2];
                    break;
                case 'SUB':
                    registers[instruction.args[0]] = args[1] - args[2];
                    break;
                case 'SUBcc':
                    registers[instruction.args[0]] = args[1] - args[2];
                    registers['FLAG'] = args[1] - args[2];
                    break;
                case 'SMUL':
                    registers[instruction.args[0]] = args[1] * args[2];
                    break;
                case 'INC':
                    registers[instruction.args[0]] += 1;
                    break;
                case 'DEC':
                    registers[instruction.args[0]] -= 1;
                    break;
                case 'SETHI':
                    registers[instruction.args[0]] = args[1] << 10;
                    break;
                case 'CLR':
                    registers[instruction.args[0]] = 0;
                    break;
                case 'CMP':
                    registers['FLAG'] = args[0] - args[1];
                    break;
                case 'BzS':
                    if (registers['FLAG'] === 0) {
                        return args[0];
                    }
                    break;
                case 'BzC':
                    if (registers['FLAG'] !== 0) {
                        return args[0];
                    }
                    break;
                case 'BA':
                    return args[0];
                    break;
                case 'NOP':
                    break;
                default:
                    console.log(`Unknown instruction: ${instruction.op}`);
            }
            return null;
        }

        function step() {
            if (instructionPointer === 0) {
                const code = document.getElementById('codeInput').value;
                const tokens = tokenize(code);
                console.log(tokens)
                parsed = parse(tokens);
                console.log(parsed)
                
                const memoryInput = document.getElementById('memoryInput').value;
                for (let i = 100; i < 110; i++) {
                    memory[i] = i+1000;
                   }
                //memory = memoryInput.split(',').map(Number); // Initialize memory from textarea
            }

            if (instructionPointer < parsed.length) {
                const output = `Executing: ${parsed[instructionPointer].op} ${parsed[instructionPointer].args.join(", ")}\n`;
                document.getElementById('output').textContent += output;

                const jump = executeInstruction(parsed[instructionPointer]);
                if (jump !== null) {
                    instructionPointer += jump;
                } else {
                    instructionPointer++;
                }

                updateRegisterTable();
                updateMemoryTextarea();
            } else {
                document.getElementById('output').textContent += "Simulation complete.\n";
            }
        }

        function updateRegisterTable() {
            const table = document.getElementById('registerTable');
            table.innerHTML = '';
            for (const [reg, value] of Object.entries(registers)) {
                table.innerHTML += `<tr><td>${reg}</td><td>${value}</td></tr>`;
            }
        }

        function updateMemoryTextarea() {
        console.log('updateMemoryTextarea',memory)
            document.getElementById('memoryInput').value = JSON.stringify(memory, null, 4);
        }
/*    </script>
</body>
</html>
*/
