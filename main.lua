local M = {}

function M:peek(job)
	local cache = ya.file_cache(job)
	if not cache then
		return
	end

	if self:preload(job) then
		ya.image_show(cache, job.area)
	end
end

function M:seek(job)
	local h = cx.active.current.hovered
	if h and h.url == job.file.url then
		local step = ya.clamp(-1, job.units, 1)
		ya.manager_emit("peek", { math.max(0, cx.active.preview.skip + step), only_if = job.file.url })
	end
end

function M:preload(job)
	local cache = ya.file_cache(job)
	if not cache or fs.cha(cache) then
		return true
	end

	local SCRIPT_PATH = os.getenv("HOME") .. "/.config/yazi/plugins/epub.yazi/epubtocover.py"
	local PYTHON = ya.target_os() == "windows" and "python" or "python3"

	local output = Command(PYTHON)
		:arg(SCRIPT_PATH)
		:arg(tostring(job.file.url))
		:stdout(Command.PIPED)
		:stderr(Command.PIPED)
		:output()

	if not output then
		return false
	elseif not output.status.success then
		local pages = tonumber(output.stderr:match("the last page %((%d+)%)")) or 0
		if job.skip > 0 and pages > 0 then
			ya.manager_emit("peek", { math.max(0, pages - 1), only_if = job.file.url, upper_bound = true })
		end
		return false
	end

	return fs.write(cache, output.stdout)
end

return M
