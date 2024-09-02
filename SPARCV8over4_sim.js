        const sw_back = document.getElementById("backend-checkbox");
        //const txt_back = document.getElementById("backend-text");
        const btn_step = document.getElementById("btn_step");
        
        const instructions = [
            "ADD", "AND", "OR", "XOR", "SUB", "ANDN", "ORN", "XNOR", "ADDX", "UMUL", "SMUL", "SUBX", "UDIV", "SDIV",
            "ADDcc", "ANDcc", "ORcc", "XORcc", "SUBcc", "ANDNcc", "ORNcc", "XNORcc", "ADDXcc", "UMULcc", "SMULcc", "SUBXcc", "UDIVcc", "SDIVcc",
            "SLL", "SRL", "SRA",
            "LD", "ST",
            "BN", "BE", "BLE", "BL", "BLEU", "BCS", "BNEG", "BVS", "BA", "BNE", "BG", "BGE", "BGU", "BCC", "BPOS", "BVC",
            "CALL", "RETL", "JMPL",
            "SETHI",
            "NOP", "MOV", "CMP", "TST", "NOT", "NEG", "INC", "DEC", "CLR",
            "BnS", "BnC", "BzS", "BzC", "BcS", "BcC", "BvS", "BvC",
            "malloc", "backend",
        ];

        const registers = { R0: 0, R1: 0, R2: 0, R3: 0, R4: 0, R5: 0, R6: 0, R7: 0 };
        let memory = registers//{R0: 0, R1: 0, R2: 0, R3: 0, R4: 0, R5: 0, R6: 0, R7: 0};

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

       function sendJson(jsonData) {
            btn_step.style.color = "red"
            btn_step.textContent  = "Wait";
            //btn_step.onclick = "";
            console.log('sendJson')
            const queryString = new URLSearchParams(jsonData).toString();

            fetch(`/api?${queryString}`)
                .then(response => response.json())  // Expecting a JSON response
                .then(data => {
                    console.log('sendJson',data);
                    btn_step.style.color = "black";
                    btn_step.textContent  = "Step";
                    //btn_step.onclick = "step()";
                    
                   
                    for (const [key, value] of Object.entries(data)) {
                        console.log(`Key: ${key}, Value: ${value}`);
                        memory[key]=parseInt(value)
                    }
                 })
                .catch(error => console.error('sendJson Error:', error));
        }


        function read_memory(address,rd){
            if (address % 4 !== 0) {
                throw new Error(`The address ${address} is not divisible by 4.`);
            }
            if (sw_back.checked) {
                //console.log('malloc..2')
                const jsonData = {
                    read_memory: [address,rd],
                    //rd:rd
                    //key2b: "value2b",
                    //key3c: "value3c"
                };

                sendJson(jsonData)
                //...
                //...
            } else{
                if (!(memory.hasOwnProperty(address))){
                            memory[address] = parseInt(prompt("Value of memory "+address, "0")); 
                        }
                return memory[address];
            }
        }

        function write_memory(address,data){
            if (address % 4 !== 0) {
                throw new Error(`The address ${address} is not divisible by 4.`);
            }
            if (sw_back.checked) {
                //console.log('malloc..2')
                const jsonData = {
                    write_memory: [address,data],
                    //key2b: "value2b",
                    //key3c: "value3c"
                };

                sendJson(jsonData)
                //...
            } else{
                memory[address] = data; 
            }
        }

        function malloc(num_bytes,rd){
            if (num_bytes % 4 !== 0) {
                throw new Error(`The number ${num_bytes} is not divisible by 4.`);
            }
            console.log('malloc..1a')
            if (sw_back.checked) {
                
                const jsonData = {
                    malloc: [num_bytes,rd],
                    //rd,rd
                    //key2b: "value2b",
                    //key3c: "value3c"
                };
                console.log('malloc..2',jsonData)
                sendJson(jsonData)
            } else{
                address=parseInt(prompt("Address of memory ", "0"));
                for (var i = 0; i < num_bytes; i=i+4) {
                    memory[address+i] = 0; 
                }
            }
        }
        

function executeInstruction(instruction) {
            const args = instruction.args.map(arg => {
                if (arg.startsWith('[')) {
                    const parts = arg.slice(1, -1).split('+');
                    const regValue = registers[parts[0]];
                    const offset = parts[1] ? parseInt(parts[1], 10) : 0;
                    return regValue + offset;
                //} else if (registers.hasOwnProperty(arg)) {
                } else if (arg.startsWith('R')) {    
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
                    //registers[instruction.args[0]] = read_memory(args[1]);
                    read_memory(args[1],instruction.args[0]);
                    break;
                case 'ST':
                    write_memory(args[0], instruction.args[1]);
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
                case 'SLL':
                    registers[instruction.args[0]] = args[1] << args[2];
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
                case 'malloc': //malloc Rd,  Cte
                        // malloc: Allocates a block of memory on the heap at runtime.
                        // Rd: Register that stores the address of the beginning of the allocated block.
                        // Cte: The number of bytes to allocate, which must be a multiple of 4 to ensure proper 4 bytes memory alignment.
                    console.log('malloc')
                    malloc(args[1],instruction.args[0])
                    break;
                case 'backend': //backend 0; backend 1
                    console.log('backend',sw_back.checked)
                    sw_back.checked=Boolean(args[0])
                    console.log('backend',sw_back.checked)
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
                for (let i = 100; i < 116; i=i+4) {
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
//Powered by ChatGPT
