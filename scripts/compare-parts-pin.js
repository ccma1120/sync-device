const fs = require('fs');
const path = require('path');

async function getPinConfigureParts() {
    // Clone repo if needed
    const repoUrl = 'https://github.com/OpenNuvoton/NuTool-PinConfigure.git';
    const repoPath = path.join(__dirname, 'NuTool-PinConfigure');
    
    if (!fs.existsSync(repoPath)) {
        console.log('Cloning PinConfigure repo...');
        await exec(`git clone ${repoUrl} ${repoPath}`);
    }

    // Parse JS files
    const jsPath = path.join(repoPath, 'src');
    const parts = new Set();
    
    const files = fs.readdirSync(jsPath).filter(f => f.endsWith('.js'));
    for (const file of files) {
        const content = fs.readFileSync(path.join(jsPath, file), 'utf8');
        // Extract part numbers from content like NUTOOL_PIN.g_cfg_chips = ['NUC980DK61Y','NUC980DK71Y', ...]
        const matches = content.match(/NUTOOL_PIN\.g_cfg_chips\s*=\s*\[(.*?)\]/s);
        if (matches) {
            const chips = matches[1]
                .split(',')
                .map(s => s.trim().replace(/['"]/g, ''))
                .filter(s => s.length > 0);
            chips.forEach(c => parts.add(c));
        }
    }
    
    return Array.from(parts);
}

async function getPartNumIDParts() {
    const content = fs.readFileSync('../source/PartNumID.cpp', 'utf8');
    const parts = new Set();
    
    // Extract part numbers from PartNumID entries
    const matches = content.matchAll(/case\s+PART_(\w+):/g);
    for (const match of matches) {
        parts.add(match[1]);
    }
    
    return Array.from(parts);
}

async function main() {
    const pinParts = await getPinConfigureParts();
    const idParts = await getPartNumIDParts();
    
    console.log('Parts in PinConfigure:', pinParts.length);
    console.log('Parts in PartNumID:', idParts.length);
    
    const missing = pinParts.filter(p => !idParts.includes(p));
    const extra = idParts.filter(p => !pinParts.includes(p));
    
    console.log('\nMissing from PartNumID:', missing);
    console.log('\nExtra in PartNumID:', extra);
    
    fs.writeFileSync('pin-parts-report.json', JSON.stringify({
        pinParts,
        idParts,
        missing,
        extra
    }, null, 2));
}

main().catch(console.error);
