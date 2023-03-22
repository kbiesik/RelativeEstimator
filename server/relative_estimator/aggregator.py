
from datetime import datetime



def aggregate_statistics(issues) -> dict:

    oldest = datetime.now()
    newest = datetime(1970, 1, 1)

    for item in issues:
        if 'resolutiondate' in item:
            date = datetime.fromisoformat(item['resolutiondate'][:10])
            if oldest > date:
                oldest = date
            if newest <= date:
                newest = date


    return {
        'count': len(issues),
        'oldest': oldest,
        'newest': newest
    }
