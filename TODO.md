# TODO: Fix Unauthorized Signup Endpoint Issue

## Tasks
- [x] Add URL alias for `/api/users/signup/` in `apps/users/urls.py` to map to `SignupView`
- [x] Update test URL in `apps/users/tests/test_api.py` to include `/api/` prefix
- [x] Run Django migrations (if needed)
- [x] Test the fix by running the dev server and simulating POST request
- [x] Run tests to ensure no regressions
