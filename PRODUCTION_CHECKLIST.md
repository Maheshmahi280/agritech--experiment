# Production Deployment Checklist

Use this checklist before deploying to production.

## Pre-Deployment (1-2 days before)

### Code Quality
- [ ] All tests passing: `python manage.py test`
- [ ] No linter errors: `pylint backend/`
- [ ] Code formatted: `black backend/`
- [ ] No debug statements left in code
- [ ] Docstrings updated for major changes
- [ ] Requirements.txt up to date
- [ ] No hardcoded secrets in code
- [ ] API endpoints tested with curl/Postman

### Security Review
- [ ] SECRET_KEY is unique and strong
- [ ] DEBUG=False in production .env
- [ ] ALLOWED_HOSTS configured correctly
- [ ] Security middleware enabled (all checked in settings.py)
- [ ] CSRF protection enabled
- [ ] SQL injection prevention checked (using ORM)
- [ ] XSS protection checked (templates escaped)
- [ ] No sensitive data in logs
- [ ] Rate limiting considered for APIs
- [ ] Input validation on all forms

### Database
- [ ] All migrations created: `python manage.py makemigrations`
- [ ] All migrations tested locally
- [ ] Backup of current database created
- [ ] Migration rollback plan documented
- [ ] Database indexes optimized
- [ ] No N+1 queries in views

### Performance
- [ ] Static files collected and tested
- [ ] Caching strategy implemented (Redis optional)
- [ ] Database queries optimized
- [ ] Assets minified (CSS/JS)
- [ ] Images optimized (JPEG, WebP)
- [ ] CDN considered for static files
- [ ] Gunicorn workers configured (3-4 for production)

### Configuration
- [ ] .env file prepared with production values
- [ ] Email configuration tested (if applicable)
- [ ] File upload limits set
- [ ] Session timeout configured
- [ ] CORS/ALLOWED_HOSTS correct
- [ ] CSRF_TRUSTED_ORIGINS configured
- [ ] DEFAULT_FROM_EMAIL configured

### Deployment Files
- [ ] Dockerfile exists and tested: `docker build -t test .`
- [ ] docker-compose.yml configured for production
- [ ] .dockerignore updated
- [ ] Health check endpoint working
- [ ] Logging configured appropriately
- [ ] Error pages (404, 500) customized

---

## Deployment Day (After hours if possible)

### Backup & Prepare
- [ ] Database backup completed: `pg_dump > backup_$(date).sql`
- [ ] Media files backed up if applicable
- [ ] Current static files backed up
- [ ] Rollback plan communicated to team
- [ ] Deployment window scheduled
- [ ] Team notified of maintenance window

### Pre-Deployment Tests
- [ ] Health check endpoint responding: `curl /health/`
- [ ] Admin interface accessible: `/admin/`
- [ ] Login/logout working
- [ ] Main dashboard page loads
- [ ] API endpoints responding (if applicable)

### Deployment
- [ ] Build Docker image: `docker build -t agriconnect:prod .`
- [ ] Test Docker image locally first
- [ ] Deploy to staging environment first
- [ ] Run all tests in staging
- [ ] Test all critical user flows in staging
- [ ] Production deployment initiated
- [ ] SSL certificate installed/verified
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic --noinput`
- [ ] Restart application services
- [ ] Verify all services running: `docker-compose ps`

### Post-Deployment Verification
- [ ] Website loads without errors
- [ ] HTTPS working correctly
- [ ] Health check passing: `curl https://domain.com/health/`
- [ ] Admin interface accessible
- [ ] Homepage displays correctly
- [ ] Forms submit successfully
- [ ] Database queries responding
- [ ] No 500 errors in logs
- [ ] Response times acceptable (<500ms)
- [ ] Static files loading (CSS, JS, images)

### Monitoring
- [ ] Error tracking service receiving events (if configured)
- [ ] Logs being captured
- [ ] CPU/Memory usage normal
- [ ] Database performance acceptable
- [ ] No rate limiting triggered
- [ ] Network connectivity stable

---

## Post-Deployment (First 24 hours)

### Monitoring & Support
- [ ] Monitor error logs hourly for first 4 hours
- [ ] Check disk space: `du -sh /app`
- [ ] Verify database size reasonable
- [ ] Check for any pending migrations
- [ ] Monitor CPU and memory usage
- [ ] Test email notifications (if applicable)
- [ ] Verify backups were created successfully

### Users & Communication
- [ ] Notify users of new deployment
- [ ] Monitor for user-reported issues
- [ ] Check support channels for complaints
- [ ] Respond to any immediate issues
- [ ] Update status page if applicable

### Rollback Readiness
- [ ] Rollback procedure confirmed working
- [ ] Previous version tagged in git
- [ ] Team trained on rollback steps
- [ ] Communication plan for rollback if needed

---

## Post-Deployment (One week)

### Performance & Stability
- [ ] No critical errors reported
- [ ] Performance metrics stable
- [ ] User adoption/activity normal
- [ ] Database backups running successfully
- [ ] Logs archived appropriately

### Documentation
- [ ] Deployment notes documented
- [ ] Any issues encountered documented
- [ ] Fixes applied documented
- [ ] Team debriefing completed
- [ ] Lessons learned captured

---

## Rollback Plan

If critical issues found during deployment:

1. **Immediate (First 5 minutes)**
   ```bash
   # Stop new deployment
   docker-compose down
   
   # Restore previous version
   git checkout previous-version-tag
   
   # Restart services
   docker-compose up -d
   ```

2. **Database Rollback (if needed)**
   ```bash
   # Restore database backup
   psql agriconnect < backup_date.sql
   ```

3. **Notify Users**
   - Send notification of temporary unavailability
   - Provide status updates
   - Apologize for inconvenience

4. **Post-Incident**
   - Investigate root cause
   - Create fix
   - Always test in staging first
   - Re-deploy when ready
   - Document learnings

---

## Production Environment Template

Create `deploy/production/.env`:

```env
SECRET_KEY=<generate-and-keep-secret>
DEBUG=False
ENVIRONMENT=production
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:password@host:5432/db
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
LOG_LEVEL=INFO
```

---

## Monitoring & Alerting

### Set up alerts for:
- [ ] Disk space < 10% (critical)
- [ ] CPU > 80% sustained
- [ ] Memory > 85% sustained
- [ ] Error rate > 1% of requests
- [ ] Response time > 1 second p95
- [ ] Database connection pool exhausted
- [ ] SSL certificate expiration < 30 days

### Daily checks:
```bash
# Check logs
docker-compose logs web --tail=100

# Check health
curl https://your-domain.com/health/

# Check database size
docker-compose exec db du -sh /var/lib/postgresql/data
```

---

## Emergency Contacts

- **Tech Lead**: [Name] - [Phone]
- **DevOps**: [Name] - [Phone]
- **Database Admin**: [Name] - [Phone]
- **Vendor Support**: [Vendor] - [Support Number]

---

## Document History

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-28 | 1.0 | Initial deployment checklist created |

---

**Last Updated**: 2026-03-28  
**Status**: Ready for Production  
**Next Review**: After first production deployment
