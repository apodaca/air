<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';

    export let cities = [];

    // Haversine formula to find distance between two lat/lon points
    function getDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // km
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLon/2) * Math.sin(dLon/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return R * c;
    }

    onMount(() => {
        // Only run on the client, and only if there's no 'area' param in the URL
        if (typeof window !== 'undefined' && navigator.geolocation && !$page.url.searchParams.has('area')) {
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    const { latitude, longitude } = pos.coords;
                    let closest = "Denver";
                    let minDistance = Infinity;

                    for (const city of cities) {
                        const dist = getDistance(latitude, longitude, city.Latitude, city.Longitude);
                        if (dist < minDistance) {
                            minDistance = dist;
                            closest = city.ReportingArea;
                        }
                    }
                    
                    // Update the URL to select the closest city
                    const newUrl = new URL(window.location.href);
                    newUrl.searchParams.set('area', closest);
                    goto(newUrl.pathname + newUrl.search, { replaceState: true });
                },
                (err) => {
                    // Fallback to Denver if permission denied or error
                    const newUrl = new URL(window.location.href);
                    newUrl.searchParams.set('area', 'Denver');
                    goto(newUrl.pathname + newUrl.search, { replaceState: true });
                }
            );
        }
    });
</script>
