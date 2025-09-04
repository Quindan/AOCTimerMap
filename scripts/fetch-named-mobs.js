#!/usr/bin/env node

/**
 * Script to fetch named mobs data from Ashes of Creation Codex API
 * Usage: node scripts/fetch-named-mobs.js
 */

const https = require('https');
const fs = require('fs');

const BASE_URL = 'https://api.ashescodex.com';
const OUTPUT_FILE = 'data/named-mobs.json';

// Ensure data directory exists
if (!fs.existsSync('data')) {
    fs.mkdirSync('data');
}

/**
 * Make HTTPS request
 */
function makeRequest(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                try {
                    const parsed = JSON.parse(data);
                    resolve(parsed);
                } catch (error) {
                    reject(error);
                }
            });
        }).on('error', (error) => {
            reject(error);
        });
    });
}

/**
 * Fetch all pages of named mobs
 */
async function fetchAllNamedMobs() {
    console.log('🔍 Fetching named mobs from Ashes Codex API...');
    
    let allMobs = [];
    let currentPage = 1;
    let totalPages = 1;
    
    try {
        // Fetch first page to get total count
        const firstPageUrl = `${BASE_URL}/mobs?page=1&per_page=30&sortColumn=name&sortDir=asc&namedMobs=true`;
        console.log(`📄 Fetching page 1...`);
        const firstPageData = await makeRequest(firstPageUrl);
        
        allMobs = allMobs.concat(firstPageData.data);
        totalPages = Math.ceil(firstPageData.meta.total / firstPageData.meta.per_page);
        
        console.log(`📊 Found ${firstPageData.meta.total} named mobs across ${totalPages} pages`);
        
        // Fetch remaining pages
        for (let page = 2; page <= totalPages; page++) {
            console.log(`📄 Fetching page ${page}/${totalPages}...`);
            const pageUrl = `${BASE_URL}/mobs?page=${page}&per_page=30&sortColumn=name&sortDir=asc&namedMobs=true`;
            const pageData = await makeRequest(pageUrl);
            allMobs = allMobs.concat(pageData.data);
            
            // Add small delay to be respectful to the API
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        
        console.log(`✅ Successfully fetched ${allMobs.length} named mobs`);
        return allMobs;
        
    } catch (error) {
        console.error('❌ Error fetching named mobs:', error.message);
        throw error;
    }
}

/**
 * Fetch detailed information for a specific mob
 */
async function fetchMobDetails(populationInstanceId) {
    try {
        const detailUrl = `${BASE_URL}/mob?populationInstanceId=${populationInstanceId}`;
        return await makeRequest(detailUrl);
    } catch (error) {
        console.warn(`⚠️ Could not fetch details for mob ${populationInstanceId}:`, error.message);
        return null;
    }
}

/**
 * Process and structure mob data
 */
function processMobData(mob) {
    const processedMob = {
        id: mob._id,
        name: mob._displayName,
        slug: mob._slug,
        levelRange: mob._levelRange,
        codexUrl: `https://ashescodex.com/entities/${mob._slug}`,
        respawnTime: null,
        respawnTimeSeconds: null,
        location: null,
        loot: mob._loot || [],
        populationInstances: []
    };
    
    // Process population instances to extract respawn times and locations
    if (mob.populationInstances && mob.populationInstances.length > 0) {
        mob.populationInstances.forEach(instance => {
            const instanceData = {
                guid: instance.guid,
                respawnTime: instance.respawnTime,
                location: instance._location,
                level: {
                    min: instance.nPCLevelMin,
                    max: instance.nPCLevelMax
                }
            };
            
            // Parse respawn time
            if (instance.respawnTime) {
                const match = instance.respawnTime.match(/(\d+)\s*seconds?/i);
                if (match) {
                    instanceData.respawnTimeSeconds = parseInt(match[1]);
                    instanceData.respawnTimeFormatted = formatRespawnTime(instanceData.respawnTimeSeconds);
                }
            }
            
            processedMob.populationInstances.push(instanceData);
        });
        
        // Use the first instance's respawn time as the main respawn time
        if (processedMob.populationInstances[0]) {
            processedMob.respawnTime = processedMob.populationInstances[0].respawnTime;
            processedMob.respawnTimeSeconds = processedMob.populationInstances[0].respawnTimeSeconds;
            processedMob.respawnTimeFormatted = processedMob.populationInstances[0].respawnTimeFormatted;
            processedMob.location = processedMob.populationInstances[0].location;
        }
    }
    
    return processedMob;
}

/**
 * Format respawn time in human-readable format
 */
function formatRespawnTime(seconds) {
    if (!seconds) return null;
    
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;
    
    if (hours > 0) {
        return `${hours}h ${minutes}m ${remainingSeconds}s`;
    } else if (minutes > 0) {
        return `${minutes}m ${remainingSeconds}s`;
    } else {
        return `${remainingSeconds}s`;
    }
}

/**
 * Main execution
 */
async function main() {
    try {
        console.log('🚀 Starting named mobs data collection...');
        
        // Fetch all named mobs
        const rawMobs = await fetchAllNamedMobs();
        
        // Process the data
        console.log('🔄 Processing mob data...');
        const processedMobs = rawMobs.map(processMobData);
        
        // Sort by name
        processedMobs.sort((a, b) => a.name.localeCompare(b.name));
        
        // Create summary statistics
        const stats = {
            totalMobs: processedMobs.length,
            mobsWithRespawnTime: processedMobs.filter(mob => mob.respawnTimeSeconds).length,
            mobsWithLocation: processedMobs.filter(mob => mob.location).length,
            uniqueRespawnTimes: [...new Set(processedMobs.map(mob => mob.respawnTimeSeconds).filter(Boolean))].sort((a, b) => a - b),
            levelRanges: [...new Set(processedMobs.map(mob => mob.levelRange).filter(Boolean))].sort()
        };
        
        // Save the data in a more memory-efficient way
        console.log('💾 Saving data...');
        
        // Save compact version without pretty printing first
        const output = {
            generatedAt: new Date().toISOString(),
            source: 'https://api.ashescodex.com/mobs',
            stats: stats,
            mobs: processedMobs.map(mob => ({
                id: mob.id,
                name: mob.name,
                slug: mob.slug,
                levelRange: mob.levelRange,
                codexUrl: mob.codexUrl,
                respawnTime: mob.respawnTime,
                respawnTimeSeconds: mob.respawnTimeSeconds,
                respawnTimeFormatted: mob.respawnTimeFormatted,
                location: mob.location
                // Skip the large loot and populationInstances arrays to reduce memory
            }))
        };
        
        fs.writeFileSync(OUTPUT_FILE, JSON.stringify(output));
        
        // Also save a summary file
        const summaryFile = 'data/named-mobs-summary.json';
        const summary = {
            generatedAt: new Date().toISOString(),
            stats: stats,
            mobsList: processedMobs.map(mob => ({
                name: mob.name,
                respawnTime: mob.respawnTimeFormatted || 'Unknown',
                codexUrl: mob.codexUrl,
                level: mob.levelRange
            }))
        };
        
        fs.writeFileSync(summaryFile, JSON.stringify(summary, null, 2));
        
        console.log('✅ Data collection complete!');
        console.log(`📊 Statistics:`);
        console.log(`   - Total named mobs: ${stats.totalMobs}`);
        console.log(`   - Mobs with respawn time: ${stats.mobsWithRespawnTime}`);
        console.log(`   - Mobs with location: ${stats.mobsWithLocation}`);
        console.log(`   - Unique respawn times: ${stats.uniqueRespawnTimes.map(t => formatRespawnTime(t)).join(', ')}`);
        console.log(`   - Level ranges: ${stats.levelRanges.join(', ')}`);
        console.log(`📁 Data saved to: ${OUTPUT_FILE}`);
        console.log(`📁 Summary saved to: ${summaryFile}`);
        
    } catch (error) {
        console.error('❌ Script failed:', error);
        process.exit(1);
    }
}

// Run the script
if (require.main === module) {
    main();
}

module.exports = { fetchAllNamedMobs, processMobData, formatRespawnTime };