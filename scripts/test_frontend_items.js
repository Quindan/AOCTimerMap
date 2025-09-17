// Script to test the new items structure in the browser console
// Run this in the browser console when on the map page

console.log('Testing new items structure...');

// Test API call
fetch('/named_mobs_api.php', {
  credentials: 'include'
})
.then(response => response.json())
.then(data => {
  console.log('API Response:', data);
  
  // Find mobs with special items
  const mobsWithItems = data.data.filter(mob => mob.special_items && mob.special_items.length > 0);
  console.log('Mobs with special items:', mobsWithItems.length);
  
  mobsWithItems.forEach(mob => {
    console.log(`${mob.name}:`, mob.special_items);
  });
})
.catch(error => {
  console.error('Error:', error);
});
