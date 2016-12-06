/*
 * hdhomerun_os_posix.c
 *
 * Copyright © 2006-2016 Silicondust USA Inc. <www.silicondust.com>.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

#include "hdhomerun_os.h"

#if defined(__APPLE__)

#include <mach/clock.h>
#include <mach/mach.h>

static pthread_once_t clock_monotonic_once = PTHREAD_ONCE_INIT;
static clock_serv_t clock_monotonic_clock_serv;

static void clock_monotonic_init(void)
{
	host_get_clock_service(mach_host_self(), SYSTEM_CLOCK, &clock_monotonic_clock_serv);
}

static inline void clock_monotonic_timespec(struct timespec *ts)
{
	pthread_once(&clock_monotonic_once, clock_monotonic_init);

	struct mach_timespec mt;
	clock_get_time(clock_monotonic_clock_serv, &mt);
	ts->tv_nsec = mt.tv_nsec;
	ts->tv_sec = mt.tv_sec;
}

static inline void clock_realtime_timespec(struct timespec *ts)
{
	struct timeval tv;
	gettimeofday(&tv, NULL);
	ts->tv_nsec = tv.tv_usec * 1000;
	ts->tv_sec = tv.tv_sec;
}

#else

static inline void clock_monotonic_timespec(struct timespec *ts)
{
	clock_gettime(CLOCK_MONOTONIC, ts);
}

static inline void clock_realtime_timespec(struct timespec *ts)
{
	clock_gettime(CLOCK_REALTIME, ts);
}

#endif

static pthread_once_t random_get32_once = PTHREAD_ONCE_INIT;
static FILE *random_get32_fp = NULL;

static void random_get32_init(void)
{
	random_get32_fp = fopen("/dev/urandom", "rb");
}

uint32_t random_get32(void)
{
	pthread_once(&random_get32_once, random_get32_init);

	if (!random_get32_fp) {
		return (uint32_t)getcurrenttime();
	}

	uint32_t Result;
	if (fread(&Result, 4, 1, random_get32_fp) != 1) {
		return (uint32_t)getcurrenttime();
	}

	return Result;
}

uint64_t getcurrenttime(void)
{
	struct timespec ts;
	clock_monotonic_timespec(&ts);
	return ((uint64_t)ts.tv_sec * 1000) + (ts.tv_nsec / 1000000);
}

void msleep_approx(uint64_t ms)
{
	uint64_t delay_s = ms / 1000;
	if (delay_s > 0) {
		sleep((unsigned int)delay_s);
		ms -= delay_s * 1000;
	}

	uint64_t delay_us = ms * 1000;
	if (delay_us > 0) {
		usleep((useconds_t)delay_us);
	}
}

void msleep_minimum(uint64_t ms)
{
	uint64_t stop_time = getcurrenttime() + ms;

	while (1) {
		uint64_t current_time = getcurrenttime();
		if (current_time >= stop_time) {
			return;
		}

		msleep_approx(stop_time - current_time);
	}
}

void pthread_mutex_dispose(pthread_mutex_t *mutex)
{
}

void thread_cond_init(thread_cond_t *cond)
{
	cond->signaled = FALSE;
	pthread_mutex_init(&cond->lock, NULL);
	pthread_cond_init(&cond->cond, NULL);
}

void thread_cond_dispose(thread_cond_t *cond)
{
}

void thread_cond_signal(thread_cond_t *cond)
{
	pthread_mutex_lock(&cond->lock);

	cond->signaled = TRUE;
	pthread_cond_signal(&cond->cond);

	pthread_mutex_unlock(&cond->lock);
}

void thread_cond_wait(thread_cond_t *cond)
{
	pthread_mutex_lock(&cond->lock);

	if (!cond->signaled) {
		pthread_cond_wait(&cond->cond, &cond->lock);
	}

	cond->signaled = FALSE;
	pthread_mutex_unlock(&cond->lock);
}

void thread_cond_wait_with_timeout(thread_cond_t *cond, uint64_t max_wait_time)
{
	pthread_mutex_lock(&cond->lock);

	if (!cond->signaled) {
		struct timespec ts;
		clock_realtime_timespec(&ts);

		uint64_t tv_nsec = (uint64_t)ts.tv_nsec + (max_wait_time * 1000000);
		ts.tv_nsec = (long)(tv_nsec % 1000000000);
		ts.tv_sec += (time_t)(tv_nsec / 1000000000);

		pthread_cond_timedwait(&cond->cond, &cond->lock, &ts);
	}

	cond->signaled = FALSE;
	pthread_mutex_unlock(&cond->lock);
}

bool_t hdhomerun_vsprintf(char *buffer, char *end, const char *fmt, va_list ap)
{
	if (buffer >= end) {
		return FALSE;
	}

	int length = vsnprintf(buffer, end - buffer - 1, fmt, ap);
	if (length < 0) {
		*buffer = 0;
		return FALSE;
	}

	if (buffer + length + 1 > end) {
		*(end - 1) = 0;
		return FALSE;

	}

	return TRUE;
}

bool_t hdhomerun_sprintf(char *buffer, char *end, const char *fmt, ...)
{
	va_list ap;
	va_start(ap, fmt);
	bool_t result = hdhomerun_vsprintf(buffer, end, fmt, ap);
	va_end(ap);
	return result;
}
