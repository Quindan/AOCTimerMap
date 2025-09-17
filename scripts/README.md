# Scripts Directory

This folder contains temporary scripts for maintenance, data processing, and one-off tasks.

## 📝 Current Scripts

### Maintenance Scripts:
- `triangulate_coordinates.py` - Recalculate named mob coordinates using reference points

### Test Scripts:
- `test_suite.py` - Suite de tests automatisés complète
- `test_endpoints.sh` - Tests rapides des endpoints avec curl
- `test_browser.py` - Tests de l'interface avec Selenium

## 🧪 Test Commands

```bash
# Tests rapides (curl only)
make test-quick

# Suite complète de tests
make test

# Tests Selenium avec Docker
make test-selenium

# Test Selenium local (nécessite: pip install selenium)
python3 scripts/test_browser.py
```

## 🔧 Maintenance Usage

```bash
# Run triangulation (requires sqlite3 and python3-numpy python3-scipy)
sudo python3 scripts/triangulate_coordinates.py

# Clean up all scripts when done
rm -rf scripts/
```

## 🧹 Cleanup Guidelines

- **Purpose**: Temporary scripts for maintenance, testing, and data processing
- **Lifecycle**: Scripts should be removed after their purpose is complete
- **Easy Cleanup**: `rm -rf scripts/` when no longer needed
- **Documentation**: Each script should have clear purpose and usage

## ⚠️ Note

This directory is meant for temporary utility scripts. Permanent application logic should go in `app/` instead.
